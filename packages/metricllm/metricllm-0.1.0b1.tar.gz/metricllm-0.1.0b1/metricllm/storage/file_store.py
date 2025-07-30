"""
File-based storage for metrics, traces, and monitoring data.
"""

import json
import os
import csv
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Union
import pickle

from metricllm.utils.logging import get_logger


class FileStore:
    """File-based storage system for MetricLLM monitoring data."""

    def __init__(self, base_path: str = "data"):
        self.base_path = base_path
        self.logger = get_logger(__name__)
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure all necessary directories exist."""
        directories = [
            self.base_path,
            os.path.join(self.base_path, "metrics"),
            os.path.join(self.base_path, "traces"),
            os.path.join(self.base_path, "evaluations"),
            os.path.join(self.base_path, "responsible_ai"),
            os.path.join(self.base_path, "monitoring"),
            os.path.join(self.base_path, "daily"),
            os.path.join(self.base_path, "exports")
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

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
            timestamp = datetime.now()

            # Save to daily file for easy querying
            daily_file = self._get_daily_file_path(timestamp)
            self._append_to_json_file(daily_file, data)

            # Save individual components
            if "metrics" in data:
                self._save_metrics(data["metrics"], trace_id, timestamp)

            if "trace" in data:
                self._save_trace(data["trace"], trace_id, timestamp)

            if "evaluations" in data:
                self._save_evaluation(data["evaluations"], trace_id, timestamp)

            if "responsible_ai" in data:
                self._save_responsible_ai(data["responsible_ai"], trace_id, timestamp)

            # Save complete monitoring record
            monitoring_file = os.path.join(self.base_path, "monitoring", f"{trace_id}.json")
            with open(monitoring_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)

            return True

        except Exception as e:
            self.logger.error(f"Failed to save monitoring data: {str(e)}")
            return False

    def _save_metrics(self, metrics: Dict[str, Any], trace_id: str, timestamp: datetime):
        """Save metrics data."""
        metrics_data = {
            "trace_id": trace_id,
            "timestamp": timestamp.isoformat(),
            **metrics
        }

        # Save to metrics directory
        metrics_file = os.path.join(self.base_path, "metrics", f"{trace_id}_metrics.json")
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, ensure_ascii=False, default=str)

        # Append to daily metrics CSV for analysis
        daily_metrics_csv = os.path.join(self.base_path, "daily", f"metrics_{timestamp.strftime('%Y%m%d')}.csv")
        self._append_metrics_to_csv(daily_metrics_csv, metrics_data)

    def _save_trace(self, trace: Dict[str, Any], trace_id: str, timestamp: datetime):
        """Save trace data."""
        trace_file = os.path.join(self.base_path, "traces", f"{trace_id}_trace.json")
        with open(trace_file, 'w', encoding='utf-8') as f:
            json.dump(trace, f, indent=2, ensure_ascii=False, default=str)

    def _save_evaluation(self, evaluations: Dict[str, Any], trace_id: str, timestamp: datetime):
        """Save evaluation data."""
        eval_data = {
            "trace_id": trace_id,
            "timestamp": timestamp.isoformat(),
            **evaluations
        }

        eval_file = os.path.join(self.base_path, "evaluations", f"{trace_id}_eval.json")
        with open(eval_file, 'w', encoding='utf-8') as f:
            json.dump(eval_data, f, indent=2, ensure_ascii=False, default=str)

    def _save_responsible_ai(self, responsible_ai: Dict[str, Any], trace_id: str, timestamp: datetime):
        """Save responsible AI data."""
        rai_data = {
            "trace_id": trace_id,
            "timestamp": timestamp.isoformat(),
            **responsible_ai
        }

        rai_file = os.path.join(self.base_path, "responsible_ai", f"{trace_id}_rai.json")
        with open(rai_file, 'w', encoding='utf-8') as f:
            json.dump(rai_data, f, indent=2, ensure_ascii=False, default=str)

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
            all_data = []

            # If specific trace IDs requested, load directly
            if trace_ids:
                for trace_id in trace_ids:
                    monitoring_file = os.path.join(self.base_path, "monitoring", f"{trace_id}.json")
                    if os.path.exists(monitoring_file):
                        with open(monitoring_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            all_data.append(data)
                return all_data

            # Load from daily files
            if start_date or end_date:
                date_range = self._get_date_range(start_date, end_date)
                for date_obj in date_range:
                    daily_file = self._get_daily_file_path(date_obj)
                    if os.path.exists(daily_file):
                        daily_data = self._load_daily_file(daily_file)
                        all_data.extend(daily_data)
            else:
                # Load all monitoring files
                monitoring_dir = os.path.join(self.base_path, "monitoring")
                for filename in os.listdir(monitoring_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(monitoring_dir, filename)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            all_data.append(data)

            # Apply filters
            filtered_data = all_data

            if providers:
                filtered_data = [d for d in filtered_data if d.get("provider") in providers]

            if models:
                filtered_data = [d for d in filtered_data if d.get("model") in models]
            return filtered_data

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
            data = self.load_monitoring_data(start_date=start_date, end_date=end_date)

            if not data:
                return {}

            # Extract metrics
            all_metrics = [d["metrics"] for d in data if "metrics" in d]

            if not all_metrics:
                return {}

            # Calculate aggregations
            summary = {
                "total_calls": len(all_metrics),
                "total_execution_time": sum(m.get("execution_time_seconds", 0) for m in all_metrics),
                "average_execution_time": 0,
                "total_tokens": sum(m.get("total_tokens", 0) for m in all_metrics),
                "total_estimated_cost": sum(m.get("estimated_cost_usd", 0) for m in all_metrics),
                "providers": {},
                "models": {},
                "performance_categories": {"fast": 0, "medium": 0, "slow": 0}
            }

            # Calculate averages
            if summary["total_calls"] > 0:
                summary["average_execution_time"] = summary["total_execution_time"] / summary["total_calls"]

            # Provider and model distributions
            for record in data:
                provider = record.get("provider", "unknown")
                model = record.get("model", "unknown")

                summary["providers"][provider] = summary["providers"].get(provider, 0) + 1
                summary["models"][model] = summary["models"].get(model, 0) + 1

            # Performance categories
            for metrics in all_metrics:
                category = metrics.get("response_time_category", "medium")
                if category in summary["performance_categories"]:
                    summary["performance_categories"][category] += 1

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

    def _get_daily_file_path(self, date_obj: datetime) -> str:
        """Get the file path for daily monitoring data."""
        return os.path.join(self.base_path, "daily", f"monitoring_{date_obj.strftime('%Y%m%d')}.json")

    def _append_to_json_file(self, filepath: str, data: Dict[str, Any]):
        """Append data to a JSON file (as array of objects)."""
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_data.append(data)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False, default=str)

    def _append_metrics_to_csv(self, filepath: str, metrics_data: Dict[str, Any]):
        """Append metrics to CSV file."""
        file_exists = os.path.exists(filepath)

        # Define CSV fields
        fields = [
            "trace_id", "timestamp", "provider", "model", "execution_time_seconds",
            "prompt_tokens", "completion_tokens", "total_tokens", "estimated_cost_usd",
            "tokens_per_second", "response_time_category"
        ]

        with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            if not file_exists:
                writer.writeheader()

            # Extract values for CSV
            row = {}
            for field in fields:
                row[field] = metrics_data.get(field, "")

            writer.writerow(row)

    def _load_daily_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Load data from a daily JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load daily file {filepath}: {str(e)}")
            return []

    def _get_date_range(self, start_date: Optional[datetime], end_date: Optional[datetime]) -> List[datetime]:
        """Get list of dates in range."""
        from datetime import timedelta

        if not start_date:
            start_date = datetime.now() - timedelta(days=30)  # Default to last 30 days
        if not end_date:
            end_date = datetime.now()

        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date)
            current_date += timedelta(days=1)

        return dates

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
