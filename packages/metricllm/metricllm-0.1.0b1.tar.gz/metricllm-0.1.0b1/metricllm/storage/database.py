"""
PostgreSQL Database Storage for MetricLLM
=========================================

Database models and storage implementation for monitoring data.
"""

import os
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class MonitoringData(Base):
    """Table for storing LLM monitoring data."""
    __tablename__ = 'monitoring_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String(50), unique=True, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    provider = Column(String(50), nullable=False, index=True)
    model = Column(String(100), nullable=False, index=True)
    function_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, index=True)  # success, error

    # Input/Output data
    prompt_data = Column(JSON)
    response_data = Column(JSON)
    error_message = Column(Text)

    # Metrics
    execution_time_seconds = Column(Float)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    total_tokens = Column(Integer)
    estimated_cost_usd = Column(Float)

    # Evaluation scores
    quality_score = Column(Float)
    coherence_score = Column(Float)
    relevance_score = Column(Float)
    completeness_score = Column(Float)

    # Responsible AI scores
    toxicity_score = Column(Float)
    bias_score = Column(Float)
    fairness_score = Column(Float)
    privacy_score = Column(Float)

    # Additional metadata
    custom_metadata = Column(JSON)


class MetricsAggregation(Base):
    """Table for storing aggregated metrics."""
    __tablename__ = 'metrics_aggregation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    provider = Column(String(50), nullable=False, index=True)
    model = Column(String(100), nullable=False, index=True)

    # Aggregated counts
    total_calls = Column(Integer, default=0)
    successful_calls = Column(Integer, default=0)
    failed_calls = Column(Integer, default=0)

    # Aggregated metrics
    total_tokens = Column(Integer, default=0)
    total_cost_usd = Column(Float, default=0.0)
    avg_response_time = Column(Float, default=0.0)

    # Average scores
    avg_quality_score = Column(Float)
    avg_coherence_score = Column(Float)
    avg_relevance_score = Column(Float)
    avg_completeness_score = Column(Float)

    # Average responsible AI scores
    avg_toxicity_score = Column(Float)
    avg_bias_score = Column(Float)
    avg_fairness_score = Column(Float)
    avg_privacy_score = Column(Float)


class PromptTemplates(Base):
    """Table for storing prompt templates."""
    __tablename__ = 'prompt_templates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    version = Column(String(50), nullable=False)
    template = Column(Text, nullable=False)
    variables = Column(JSON)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)


class DatabaseStorage:
    """PostgreSQL database storage for MetricLLM."""

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")

        # Configure engine with connection pooling and SSL handling
        engine_kwargs = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "connect_args": {"sslmode": "prefer"}
        }

        self.engine = create_engine(self.database_url, **engine_kwargs)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Create tables
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()

    def store_monitoring_data(self, data: Dict[str, Any]) -> str:
        """Store monitoring data in the database."""
        with self.get_session() as session:
            # Extract data fields
            trace_id = data.get("trace_id", str(uuid.uuid4()))

            monitoring_record = MonitoringData(
                trace_id=trace_id,
                timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now(timezone.utc).isoformat())),
                provider=data.get("provider", "unknown"),
                model=data.get("model", "unknown"),
                function_name=data.get("function_name", "unknown"),
                status=data.get("status", "unknown"),

                # Input/Output
                prompt_data=data.get("prompt_data"),
                response_data=data.get("response_data"),
                error_message=data.get("error_message"),

                # Metrics
                execution_time_seconds=data.get("metrics", {}).get("execution_time_seconds"),
                prompt_tokens=data.get("metrics", {}).get("prompt_tokens"),
                completion_tokens=data.get("metrics", {}).get("completion_tokens"),
                total_tokens=data.get("metrics", {}).get("total_tokens"),
                estimated_cost_usd=data.get("metrics", {}).get("estimated_cost_usd"),

                # Evaluation scores
                quality_score=data.get("evaluation", {}).get("overall_score"),
                coherence_score=data.get("evaluation", {}).get("coherence", {}).get("score"),
                relevance_score=data.get("evaluation", {}).get("relevance", {}).get("score"),
                completeness_score=data.get("evaluation", {}).get("completeness", {}).get("score"),

                # Responsible AI scores
                toxicity_score=data.get("responsible_ai", {}).get("toxicity_score"),
                bias_score=data.get("responsible_ai", {}).get("bias_score"),
                fairness_score=data.get("responsible_ai", {}).get("fairness_score"),
                privacy_score=data.get("responsible_ai", {}).get("privacy_score"),

                # Metadata
                custom_metadata=data.get("custom_metadata")
            )

            session.add(monitoring_record)
            session.commit()

            return trace_id

    def get_monitoring_data(self,
                            days_back: int = 7,
                            provider: Optional[str] = None,
                            model: Optional[str] = None,
                            status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve monitoring data from the database."""
        with self.get_session() as session:
            query = session.query(MonitoringData)

            # Apply filters
            if days_back > 0:
                cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
                query = query.filter(MonitoringData.timestamp >= cutoff_date)

            if provider:
                query = query.filter(MonitoringData.provider == provider)

            if model:
                query = query.filter(MonitoringData.model == model)

            if status:
                query = query.filter(MonitoringData.status == status)

            # Order by timestamp descending
            query = query.order_by(MonitoringData.timestamp.desc())

            results = []
            for record in query.all():
                data = {
                    "trace_id": record.trace_id,
                    "timestamp": record.timestamp.isoformat(),
                    "provider": record.provider,
                    "model": record.model,
                    "function_name": record.function_name,
                    "status": record.status,
                    "prompt_data": record.prompt_data,
                    "response_data": record.response_data,
                    "error_message": record.error_message,
                    "metrics": {
                        "execution_time_seconds": record.execution_time_seconds,
                        "prompt_tokens": record.prompt_tokens,
                        "completion_tokens": record.completion_tokens,
                        "total_tokens": record.total_tokens,
                        "estimated_cost_usd": record.estimated_cost_usd,
                    },
                    "evaluation": {
                        "overall_score": record.quality_score,
                        "coherence": {"score": record.coherence_score},
                        "relevance": {"score": record.relevance_score},
                        "completeness": {"score": record.completeness_score},
                    },
                    "responsible_ai": {
                        "toxicity_score": record.toxicity_score,
                        "bias_score": record.bias_score,
                        "fairness_score": record.fairness_score,
                        "privacy_score": record.privacy_score,
                    },
                    "custom_metadata": record.custom_metadata
                }
                results.append(data)

            return results

    def store_prompt_template(self, name: str, template: str, variables: List[str],
                              description: str = "", version: Optional[str] = None) -> str:
        """Store a prompt template in the database."""
        with self.get_session() as session:
            if not version:
                version = str(uuid.uuid4())[:8]

            # Deactivate previous versions
            session.query(PromptTemplates).filter(
                PromptTemplates.name == name,
                PromptTemplates.is_active == True
            ).update({"is_active": False})

            prompt_template = PromptTemplates(
                name=name,
                version=version,
                template=template,
                variables=variables,
                description=description,
                is_active=True
            )

            session.add(prompt_template)
            session.commit()

            return version

    def get_prompt_template(self, name: str, version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Retrieve a prompt template from the database."""
        with self.get_session() as session:
            query = session.query(PromptTemplates).filter(PromptTemplates.name == name)

            if version:
                query = query.filter(PromptTemplates.version == version)
            else:
                query = query.filter(PromptTemplates.is_active == True)

            record = query.first()

            if record:
                return {
                    "name": record.name,
                    "version": record.version,
                    "template": record.template,
                    "variables": record.variables,
                    "description": record.description,
                    "created_at": record.created_at.isoformat(),
                    "is_active": record.is_active
                }

            return None

    def get_all_prompt_templates(self) -> List[Dict[str, Any]]:
        """Get all active prompt templates."""
        with self.get_session() as session:
            records = session.query(PromptTemplates).filter(
                PromptTemplates.is_active == True
            ).order_by(PromptTemplates.created_at.desc()).all()

            return [
                {
                    "name": record.name,
                    "version": record.version,
                    "template": record.template,
                    "variables": record.variables,
                    "description": record.description,
                    "created_at": record.created_at.isoformat(),
                    "is_active": record.is_active
                }
                for record in records
            ]

    def get_aggregated_metrics(self, days_back: int = 30) -> Dict[str, Any]:
        """Get aggregated metrics from monitoring data."""
        with self.get_session() as session:
            from sqlalchemy import func
            from datetime import timedelta

            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)

            # Overall metrics
            total_calls = session.query(func.count(MonitoringData.id)).filter(
                MonitoringData.timestamp >= cutoff_date
            ).scalar() or 0

            successful_calls = session.query(func.count(MonitoringData.id)).filter(
                MonitoringData.timestamp >= cutoff_date,
                MonitoringData.status == "success"
            ).scalar() or 0

            # Provider breakdown
            provider_stats = session.query(
                MonitoringData.provider,
                func.count(MonitoringData.id).label('call_count'),
                func.avg(MonitoringData.execution_time_seconds).label('avg_response_time'),
                func.sum(MonitoringData.total_tokens).label('total_tokens'),
                func.sum(MonitoringData.estimated_cost_usd).label('total_cost')
            ).filter(
                MonitoringData.timestamp >= cutoff_date
            ).group_by(MonitoringData.provider).all()

            # Model breakdown
            model_stats = session.query(
                MonitoringData.model,
                func.count(MonitoringData.id).label('call_count'),
                func.avg(MonitoringData.quality_score).label('avg_quality')
            ).filter(
                MonitoringData.timestamp >= cutoff_date
            ).group_by(MonitoringData.model).all()

            return {
                "total_calls": total_calls,
                "successful_calls": successful_calls,
                "success_rate": (successful_calls / total_calls * 100) if total_calls > 0 else 0,
                "provider_stats": [
                    {
                        "provider": stat.provider,
                        "call_count": stat.call_count,
                        "avg_response_time": float(stat.avg_response_time or 0),
                        "total_tokens": int(stat.total_tokens or 0),
                        "total_cost": float(stat.total_cost or 0)
                    }
                    for stat in provider_stats
                ],
                "model_stats": [
                    {
                        "model": stat.model,
                        "call_count": stat.call_count,
                        "avg_quality": float(stat.avg_quality or 0)
                    }
                    for stat in model_stats
                ]
            }


# Global database instance
_db_storage = None


def get_database_storage() -> DatabaseStorage:
    """Get the global database storage instance."""
    global _db_storage
    if _db_storage is None:
        _db_storage = DatabaseStorage()
    return _db_storage
