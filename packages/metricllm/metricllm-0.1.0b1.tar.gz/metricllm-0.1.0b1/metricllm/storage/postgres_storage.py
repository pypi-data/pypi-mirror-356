"""
PostgreSQL database storage for metrics, traces, and monitoring data.
"""

import json
import os
import csv
import psycopg2
import psycopg2.extras
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional, Union
import pickle
from contextlib import contextmanager

from metricllm.utils.logging import get_logger


class PostgresStore:
    """PostgreSQL-based storage system for MetricLLM monitoring data."""

    def __init__(self,
                 host: str = "localhost",
                 port: int = 5432,
                 database: str = "metricllm",
                 username: str = "postgres",
                 password: str = "",
                 base_path: str = "data"):
        """
        Initialize PostgreSQL connection.

        Args:
            host: Database host
            port: Database port
            database: Database name
            username: Database username
            password: Database password
            base_path: Base path for exports (maintains compatibility with FileStore)
        """
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.base_path = base_path
        self.logger = get_logger(__name__)

        # Initialize database connection and create tables
        self._init_database()
        self._ensure_directories()

    def _init_database(self):
        """Initialize database connection and create tables if they don't exist."""
        try:
            # Test connection
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version();")
                    version = cur.fetchone()
                    self.logger.info(f"Connected to PostgreSQL: {version[0]}")

            # Create tables
            self._create_tables()

        except Exception as e:
            self.logger.error(f"Failed to initialize database: {str(e)}")
            raise

    @contextmanager
    def _get_connection(self):
        """Get database connection context manager."""
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password
            )
            conn.autocommit = False
            yield conn
        finally:
            if conn:
                conn.close()

    def _create_tables(self):
        """Create database tables if they don't exist."""
        create_tables_sql = """
        -- Main monitoring data table
        CREATE TABLE IF NOT EXISTS monitoring_data (
            trace_id VARCHAR(255) PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            function_name VARCHAR(255),
            provider VARCHAR(100),
            model VARCHAR(255),
            status VARCHAR(50),
            data JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Metrics table for easier querying and aggregation
        CREATE TABLE IF NOT EXISTS metrics (
            id SERIAL PRIMARY KEY,
            trace_id VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            provider VARCHAR(100),
            model VARCHAR(255),
            execution_time_seconds DECIMAL(10,6),
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_tokens INTEGER,
            estimated_cost_usd DECIMAL(10,6),
            tokens_per_second DECIMAL(10,2),
            response_time_category VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trace_id) REFERENCES monitoring_data(trace_id) ON DELETE CASCADE
        );

        -- Traces table
        CREATE TABLE IF NOT EXISTS traces (
            id SERIAL PRIMARY KEY,
            trace_id VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            trace_data JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trace_id) REFERENCES monitoring_data(trace_id) ON DELETE CASCADE
        );

        -- Evaluations table
        CREATE TABLE IF NOT EXISTS evaluations (
            id SERIAL PRIMARY KEY,
            trace_id VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            overall_score DECIMAL(5,3),
            evaluation_data JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trace_id) REFERENCES monitoring_data(trace_id) ON DELETE CASCADE
        );

        -- Responsible AI table
        CREATE TABLE IF NOT EXISTS responsible_ai (
            id SERIAL PRIMARY KEY,
            trace_id VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            overall_safety_score DECIMAL(5,3),
            safety_level VARCHAR(50),
            rai_data JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trace_id) REFERENCES monitoring_data(trace_id) ON DELETE CASCADE
        );

        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_monitoring_data_timestamp ON monitoring_data(timestamp);
        CREATE INDEX IF NOT EXISTS idx_monitoring_data_provider ON monitoring_data(provider);
        CREATE INDEX IF NOT EXISTS idx_monitoring_data_model ON monitoring_data(model);
        CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp);
        CREATE INDEX IF NOT EXISTS idx_metrics_provider ON metrics(provider);
        CREATE INDEX IF NOT EXISTS idx_metrics_model ON metrics(model);
        """

        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(create_tables_sql)
                conn.commit()
                self.logger.info("Database tables created successfully")
        except Exception as e:
            self.logger.error(f"Failed to create tables: {str(e)}")
            raise

    def _ensure_directories(self):
        """Ensure export directory exists."""
        export_dir = os.path.join(self.base_path, "exports")
        os.makedirs(export_dir, exist_ok=True)

    def save_monitoring_data(self, data: Dict[str, Any]) -> bool:
        """
        Save comprehensive monitoring data.

        Args:
            data: Complete monitoring data dictionary

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            trace_id = data.get("trace_id", "unknown")
            timestamp = data.get("timestamp", datetime.now().isoformat())

            # Convert string timestamp to datetime if needed
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    # Insert main monitoring data
                    cur.execute("""
                        INSERT INTO monitoring_data 
                        (trace_id, timestamp, function_name, provider, model, status, data)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (trace_id) 
                        DO UPDATE SET 
                            timestamp = EXCLUDED.timestamp,
                            function_name = EXCLUDED.function_name,
                            provider = EXCLUDED.provider,
                            model = EXCLUDED.model,
                            status = EXCLUDED.status,
                            data = EXCLUDED.data
                    """, (
                        trace_id,
                        timestamp,
                        data.get("function_name"),
                        data.get("provider"),
                        data.get("model"),
                        data.get("status"),
                        json.dumps(data)
                    ))

                    # Save individual components
                    if "metrics" in data:
                        self._save_metrics_db(cur, data["metrics"], trace_id, timestamp)

                    if "trace" in data:
                        self._save_trace_db(cur, data["trace"], trace_id, timestamp)

                    if "evaluations" in data:
                        self._save_evaluation_db(cur, data["evaluations"], trace_id, timestamp)

                    if "responsible_ai" in data:
                        self._save_responsible_ai_db(cur, data["responsible_ai"], trace_id, timestamp)

                conn.commit()
                return True

        except Exception as e:
            self.logger.error(f"Failed to save monitoring data: {str(e)}")
            return False

    def _save_metrics_db(self, cur, metrics: Dict[str, Any], trace_id: str, timestamp: datetime):
        """Save metrics data to database."""
        cur.execute("""
            INSERT INTO metrics 
            (trace_id, timestamp, provider, model, execution_time_seconds, 
             prompt_tokens, completion_tokens, total_tokens, estimated_cost_usd,
             tokens_per_second, response_time_category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (trace_id) 
            DO UPDATE SET 
                timestamp = EXCLUDED.timestamp,
                provider = EXCLUDED.provider,
                model = EXCLUDED.model,
                execution_time_seconds = EXCLUDED.execution_time_seconds,
                prompt_tokens = EXCLUDED.prompt_tokens,
                completion_tokens = EXCLUDED.completion_tokens,
                total_tokens = EXCLUDED.total_tokens,
                estimated_cost_usd = EXCLUDED.estimated_cost_usd,
                tokens_per_second = EXCLUDED.tokens_per_second,
                response_time_category = EXCLUDED.response_time_category
        """, (
            trace_id,
            timestamp,
            metrics.get("provider"),
            metrics.get("model"),
            metrics.get("execution_time_seconds"),
            metrics.get("prompt_tokens"),
            metrics.get("completion_tokens"),
            metrics.get("total_tokens"),
            metrics.get("estimated_cost_usd"),
            metrics.get("tokens_per_second"),
            metrics.get("response_time_category")
        ))

    def _save_trace_db(self, cur, trace: Dict[str, Any], trace_id: str, timestamp: datetime):
        """Save trace data to database."""
        cur.execute("""
            INSERT INTO traces (trace_id, timestamp, trace_data)
            VALUES (%s, %s, %s)
            ON CONFLICT (trace_id) 
            DO UPDATE SET 
                timestamp = EXCLUDED.timestamp,
                trace_data = EXCLUDED.trace_data
        """, (trace_id, timestamp, json.dumps(trace)))

    def _save_evaluation_db(self, cur, evaluations: Dict[str, Any], trace_id: str, timestamp: datetime):
        """Save evaluation data to database."""
        cur.execute("""
            INSERT INTO evaluations (trace_id, timestamp, overall_score, evaluation_data)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (trace_id) 
            DO UPDATE SET 
                timestamp = EXCLUDED.timestamp,
                overall_score = EXCLUDED.overall_score,
                evaluation_data = EXCLUDED.evaluation_data
        """, (
            trace_id,
            timestamp,
            evaluations.get("overall_score"),
            json.dumps(evaluations)
        ))

    def _save_responsible_ai_db(self, cur, responsible_ai: Dict[str, Any], trace_id: str, timestamp: datetime):
        """Save responsible AI data to database."""
        cur.execute("""
            INSERT INTO responsible_ai (trace_id, timestamp, overall_safety_score, safety_level, rai_data)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (trace_id) 
            DO UPDATE SET 
                timestamp = EXCLUDED.timestamp,
                overall_safety_score = EXCLUDED.overall_safety_score,
                safety_level = EXCLUDED.safety_level,
                rai_data = EXCLUDED.rai_data
        """, (
            trace_id,
            timestamp,
            responsible_ai.get("overall_safety_score"),
            responsible_ai.get("safety_level"),
            json.dumps(responsible_ai)
        ))

    def load_monitoring_data(self,
                             start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None,
                             trace_ids: Optional[List[str]] = None,
                             providers: Optional[List[str]] = None,
                             models: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Load monitoring data with optional filtering.

        Args:
            start_date: Filter by start date
            end_date: Filter by end date
            trace_ids: Filter by specific trace IDs
            providers: Filter by providers
            models: Filter by models

        Returns:
            List of monitoring data records
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    # Build query with filters
                    query = "SELECT * FROM monitoring_data WHERE 1=1"
                    params = []

                    if start_date:
                        query += " AND timestamp >= %s"
                        params.append(start_date)

                    if end_date:
                        query += " AND timestamp <= %s"
                        params.append(end_date)

                    if trace_ids:
                        query += " AND trace_id = ANY(%s)"
                        params.append(trace_ids)

                    if providers:
                        query += " AND provider = ANY(%s)"
                        params.append(providers)

                    if models:
                        query += " AND model = ANY(%s)"
                        params.append(models)

                    query += " ORDER BY timestamp DESC"

                    cur.execute(query, params)
                    rows = cur.fetchall()

                    # Convert rows to dictionaries and parse JSON data
                    result = []
                    for row in rows:
                        data = dict(row)
                        # Parse the JSON data field
                        if 'data' in data and data['data']:
                            json_data = data['data']
                            if isinstance(json_data, str):
                                json_data = json.loads(json_data)

                            # Merge the JSON data with the row data
                            result.append(json_data)
                        else:
                            result.append(data)

                    return result

        except Exception as e:
            self.logger.error(f"Failed to load monitoring data: {str(e)}")
            return []

    def get_metrics_summary(self,
                            start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get aggregated metrics summary.

        Args:
            start_date: Start date for summary
            end_date: End date for summary

        Returns:
            Metrics summary dictionary
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    # Build query with date filters
                    where_clause = "WHERE 1=1"
                    params = []

                    if start_date:
                        where_clause += " AND timestamp >= %s"
                        params.append(start_date)

                    if end_date:
                        where_clause += " AND timestamp <= %s"
                        params.append(end_date)

                    # Get aggregated metrics
                    cur.execute(f"""
                        SELECT 
                            COUNT(*) as total_calls,
                            SUM(execution_time_seconds) as total_execution_time,
                            AVG(execution_time_seconds) as average_execution_time,
                            SUM(total_tokens) as total_tokens,
                            SUM(estimated_cost_usd) as total_estimated_cost
                        FROM metrics 
                        {where_clause}
                    """, params)

                    metrics_agg = cur.fetchone()

                    # Get provider distribution
                    cur.execute(f"""
                        SELECT provider, COUNT(*) as count
                        FROM metrics 
                        {where_clause}
                        GROUP BY provider
                    """, params)

                    providers_data = cur.fetchall()

                    # Get model distribution
                    cur.execute(f"""
                        SELECT model, COUNT(*) as count
                        FROM metrics 
                        {where_clause}
                        GROUP BY model
                    """, params)

                    models_data = cur.fetchall()

                    # Get performance categories
                    cur.execute(f"""
                        SELECT response_time_category, COUNT(*) as count
                        FROM metrics 
                        {where_clause}
                        GROUP BY response_time_category
                    """, params)

                    performance_data = cur.fetchall()

                    # Build summary
                    summary = {
                        "total_calls": metrics_agg["total_calls"] or 0,
                        "total_execution_time": float(metrics_agg["total_execution_time"] or 0),
                        "average_execution_time": float(metrics_agg["average_execution_time"] or 0),
                        "total_tokens": metrics_agg["total_tokens"] or 0,
                        "total_estimated_cost": float(metrics_agg["total_estimated_cost"] or 0),
                        "providers": {row["provider"]: row["count"] for row in providers_data},
                        "models": {row["model"]: row["count"] for row in models_data},
                        "performance_categories": {row["response_time_category"]: row["count"] for row in
                                                   performance_data}
                    }

                    return summary

        except Exception as e:
            self.logger.error(f"Failed to generate metrics summary: {str(e)}")
            return {}

    def export_data(self,
                    format_type: str = "json",
                    start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None,
                    data_types: Optional[List[str]] = None) -> Optional[str]:
        """
        Export data to various formats.

        Args:
            format_type: Export format ("json", "csv", "pickle")
            start_date: Start date for export
            end_date: End date for export
            data_types: Types of data to export ("metrics", "traces", "evaluations", "responsible_ai")

        Returns:
            Path to exported file or None if failed
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if format_type == "json":
                return self._export_json(timestamp, start_date, end_date, data_types)
            elif format_type == "csv":
                return self._export_csv(timestamp, start_date, end_date, data_types)
            elif format_type == "pickle":
                return self._export_pickle(timestamp, start_date, end_date, data_types)
            else:
                self.logger.error(f"Unsupported export format: {format_type}")
                return None

        except Exception as e:
            self.logger.error(f"Export failed: {str(e)}")
            return None

    def _export_json(self, timestamp: str, start_date: Optional[datetime], end_date: Optional[datetime],
                     data_types: Optional[List[str]]) -> str:
        """Export data as JSON."""
        data = self.load_monitoring_data(start_date=start_date, end_date=end_date)

        export_file = os.path.join(self.base_path, "exports", f"export_{timestamp}.json")
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        return export_file

    def _export_csv(self, timestamp: str, start_date: Optional[datetime], end_date: Optional[datetime],
                    data_types: Optional[List[str]]) -> str:
        """Export data as CSV."""
        data = self.load_monitoring_data(start_date=start_date, end_date=end_date)

        export_file = os.path.join(self.base_path, "exports", f"export_{timestamp}.csv")

        if not data:
            return export_file

        # Flatten data for CSV
        flattened_data = []
        for record in data:
            flat_record = {
                "trace_id": record.get("trace_id", ""),
                "timestamp": record.get("timestamp", ""),
                "function_name": record.get("function_name", ""),
                "provider": record.get("provider", ""),
                "model": record.get("model", ""),
                "status": record.get("status", "")
            }

            # Add metrics
            if "metrics" in record:
                metrics = record["metrics"]
                flat_record.update({
                    "execution_time": metrics.get("execution_time_seconds", 0),
                    "total_tokens": metrics.get("total_tokens", 0),
                    "estimated_cost": metrics.get("estimated_cost_usd", 0),
                    "tokens_per_second": metrics.get("tokens_per_second", 0)
                })

            # Add evaluation scores
            if "evaluations" in record:
                evaluations = record["evaluations"]
                flat_record["overall_evaluation_score"] = evaluations.get("overall_score", 0)

            # Add responsible AI scores
            if "responsible_ai" in record:
                rai = record["responsible_ai"]
                flat_record["safety_score"] = rai.get("overall_safety_score", 0)
                flat_record["safety_level"] = rai.get("safety_level", "")

            flattened_data.append(flat_record)

        # Write CSV
        if flattened_data:
            with open(export_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=flattened_data[0].keys())
                writer.writeheader()
                writer.writerows(flattened_data)

        return export_file

    def _export_pickle(self, timestamp: str, start_date: Optional[datetime], end_date: Optional[datetime],
                       data_types: Optional[List[str]]) -> str:
        """Export data as pickle."""
        data = self.load_monitoring_data(start_date=start_date, end_date=end_date)

        export_file = os.path.join(self.base_path, "exports", f"export_{timestamp}.pkl")
        with open(export_file, 'wb') as f:
            pickle.dump(data, f)

        return export_file

    def close(self):
        """Close database connections (for cleanup)."""
        # PostgreSQL connections are handled by context managers
        # This method is provided for interface compatibility
        pass


# Factory function to create storage instance based on configuration
def create_storage(storage_type: str = "file", **kwargs):
    """
    Factory function to create storage instance.

    Args:
        storage_type: "file" or "postgres"
        **kwargs: Storage-specific configuration

    Returns:
        Storage instance (FileStore or PostgresStore)
    """
    if storage_type.lower() == "file":
        from .file_storage import FileStore
        return FileStore(base_path=kwargs.get("base_path", "data"))
    elif storage_type.lower() == "postgres":
        return PostgresStore(
            host=kwargs.get("host", "localhost"),
            port=kwargs.get("port", 5432),
            database=kwargs.get("database", "metricllm"),
            username=kwargs.get("username", "postgres"),
            password=kwargs.get("password", ""),
            base_path=kwargs.get("base_path", "data")
        )
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")