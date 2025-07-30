"""
Core monitoring decorator for LLM interactions.
"""

import functools
import time
import hashlib
import json
from datetime import datetime
from typing import Any, Callable, Dict, Optional

# Core modules for monitoring
from metricllm.core.metrics import MetricsCollector
from metricllm.core.traces import TraceLogger
from metricllm.core.evaluations import EvaluationFramework
from metricllm.core.responsible_ai import ResponsibleAI

# Import storage configuration
from metricllm.storage.config import StorageConfig

# Logging
from metricllm.utils.logging import get_logger


class MonitoringDecorator:
    """
    Main decorator class that monitors LLM function calls by:
    - Tracking metrics (latency, tokens, cost)
    - Logging traces
    - Evaluating responses
    - Checking responsible AI usage
    - Persisting all monitoring data using configured storage backend
    """

    def __init__(self, storage_config: Optional[StorageConfig] = None):
        """
        Initialize the monitoring decorator.

        Args:
            storage_config: Optional custom storage configuration.
                          If None, uses default configuration from environment.
        """
        self.metrics_collector = MetricsCollector()
        self.trace_logger = TraceLogger()
        self.evaluation_framework = EvaluationFramework()
        self.responsible_ai = ResponsibleAI()
        self.logger = get_logger(__name__)

        # Initialize storage using config
        if storage_config is None:
            storage_config = StorageConfig()

        self.storage_config = storage_config

        try:
            self.storage = storage_config.create_storage()
            self.logger.info(f"Storage initialized successfully: {storage_config.storage_type}")
        except Exception as e:
            self.logger.error(f"Failed to initialize storage: {e}")
            # Fallback to file storage if configured storage fails
            try:
                from metricllm.storage.file_storage import FileStore
                self.storage = FileStore()
                self.logger.warning("Fallback to file storage activated")
            except Exception as fallback_error:
                self.logger.critical(f"Failed to initialize fallback storage: {fallback_error}")
                raise

    def __call__(self,
                 provider: str = "openai",
                 model: str = "gpt-3.5-turbo",
                 track_tokens: bool = True,
                 track_cost: bool = True,
                 evaluate: bool = True,
                 responsible_ai_check: bool = True,
                 log_level: str = "INFO",
                 custom_metadata: Optional[Dict] = None) -> Callable:
        """
        Decorator for monitoring LLM function calls.

        Args:
            provider: LLM provider (e.g., openai, anthropic)
            model: LLM model name
            track_tokens: Enable token tracking
            track_cost: Enable cost estimation
            evaluate: Run evaluation framework
            responsible_ai_check: Run responsible AI checks
            log_level: Logging verbosity level
            custom_metadata: Optional custom metadata to include
        """

        def decorator(func: Callable) -> Callable:

            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                trace_id = self._generate_trace_id(func.__name__, args, kwargs)
                start_time = time.time()

                prompt_data = self._extract_prompt_data(args, kwargs)

                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    response_data = self._extract_response_data(result)

                    # Collect metrics
                    metrics = self.metrics_collector.collect(
                        provider=provider,
                        model=model,
                        prompt=prompt_data.get("prompt", ""),
                        response=response_data.get("response", ""),
                        execution_time=execution_time,
                        track_tokens=track_tokens,
                        track_cost=track_cost
                    )

                    # Log trace
                    trace = self.trace_logger.log_trace(
                        trace_id=trace_id,
                        function_name=func.__name__,
                        provider=provider,
                        model=model,
                        prompt_data=prompt_data,
                        response_data=response_data,
                        metrics=metrics,
                        execution_time=execution_time,
                        custom_metadata=custom_metadata
                    )

                    # Evaluation framework
                    evaluation_results = {}
                    if evaluate:
                        evaluation_results = self.evaluation_framework.evaluate(
                            prompt=prompt_data.get("prompt", ""),
                            response=response_data.get("response", ""),
                            provider=provider,
                            model=model
                        )

                    # Responsible AI check
                    responsible_ai_results = {}
                    if responsible_ai_check:
                        responsible_ai_results = self.responsible_ai.check(
                            prompt=prompt_data.get("prompt", ""),
                            response=response_data.get("response", "")
                        )

                    # Consolidate monitoring data
                    monitoring_data = {
                        "trace_id": trace_id,
                        "timestamp": datetime.now().isoformat(),
                        "function_name": func.__name__,
                        "provider": provider,
                        "model": model,
                        "prompt_data": prompt_data,
                        "response_data": response_data,
                        "metrics": metrics,
                        "trace": trace,
                        "evaluations": evaluation_results,  # Changed from "evaluation" to match storage schema
                        "responsible_ai": responsible_ai_results,
                        "status": "success",
                        "custom_metadata": custom_metadata
                    }

                    # Store data using configured storage backend
                    success = self.storage.save_monitoring_data(monitoring_data)

                    if success:
                        self.logger.info(
                            f"LLM call monitored successfully - Trace ID: {trace_id}, Storage: {self.storage_config.storage_type}")
                    else:
                        self.logger.warning(f"Failed to save monitoring data - Trace ID: {trace_id}")

                    return result

                except Exception as e:
                    execution_time = time.time() - start_time

                    error_data = {
                        "trace_id": trace_id,
                        "timestamp": datetime.now().isoformat(),
                        "function_name": func.__name__,
                        "provider": provider,
                        "model": model,
                        "error_message": str(e),
                        "metrics": {"execution_time_seconds": execution_time},
                        "status": "error",
                        "custom_metadata": custom_metadata
                    }

                    # Store error data using configured storage backend
                    try:
                        self.storage.save_monitoring_data(error_data)
                        self.logger.error(
                            f"LLM call failed - Trace ID: {trace_id}, Error: {str(e)}, Storage: {self.storage_config.storage_type}")
                    except Exception as storage_error:
                        self.logger.critical(
                            f"Failed to save error data - Trace ID: {trace_id}, Storage Error: {storage_error}")

                    raise

            return wrapper

        return decorator

    def _generate_trace_id(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate a short unique trace ID from function name and arguments."""
        data = f"{time.time()}_{func_name}_{args}_{kwargs}"
        return hashlib.md5(data.encode()).hexdigest()[:16]

    def _extract_prompt_data(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """Extract prompt and relevant input parameters from args/kwargs."""
        prompt_data = {}

        # Check common prompt patterns
        if args:
            if isinstance(args[0], str):
                prompt_data["prompt"] = args[0]
            elif isinstance(args[0], dict) and "messages" in args[0]:
                prompt_data["prompt"] = json.dumps(args[0]["messages"])

        for key in ["prompt", "messages", "input", "query", "text"]:
            if key in kwargs:
                val = kwargs[key]
                prompt_data["prompt"] = val if isinstance(val, str) else json.dumps(val)
                break

        for param in ["temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty"]:
            if param in kwargs:
                prompt_data[param] = kwargs[param]

        return prompt_data

    def _extract_response_data(self, result: Any) -> Dict[str, Any]:
        """Extract relevant response content and usage from result."""
        response_data = {}

        if isinstance(result, str):
            response_data["response"] = result

        elif isinstance(result, dict):
            # Handle dict responses (e.g., OpenAI format)
            choices = result.get("choices", [])
            if choices:
                choice = choices[0]
                if "message" in choice:
                    response_data["response"] = choice["message"].get("content", "")
                elif "text" in choice:
                    response_data["response"] = choice["text"]

            if "usage" in result:
                response_data["usage"] = result["usage"]

        elif hasattr(result, "choices"):
            choice = result.choices[0]
            if hasattr(choice, "message"):
                response_data["response"] = choice.message.content
            elif hasattr(choice, "text"):
                response_data["response"] = choice.text

            if hasattr(result, "usage"):
                usage = result.usage
                response_data["usage"] = {
                    "prompt_tokens": getattr(usage, "prompt_tokens", 0),
                    "completion_tokens": getattr(usage, "completion_tokens", 0),
                    "total_tokens": getattr(usage, "total_tokens", 0)
                }

        return response_data

    def get_storage_info(self) -> Dict[str, str]:
        """Get information about the current storage configuration."""
        return {
            "storage_type": self.storage_config.storage_type,
            "storage_class": self.storage.__class__.__name__
        }

    def switch_storage(self, new_config: StorageConfig) -> bool:
        """
        Switch to a different storage backend.

        Args:
            new_config: New storage configuration

        Returns:
            True if switch was successful, False otherwise
        """
        try:
            # Close current storage if it has a close method
            if hasattr(self.storage, 'close'):
                self.storage.close()

            # Create new storage
            new_storage = new_config.create_storage()

            # Update configuration and storage
            self.storage_config = new_config
            self.storage = new_storage

            self.logger.info(f"Successfully switched to storage: {new_config.storage_type}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to switch storage: {e}")
            return False


# Factory function to create monitoring decorator with specific storage config
def create_monitor(storage_type: str = None, **storage_kwargs) -> MonitoringDecorator:
    """
    Create a monitoring decorator with specific storage configuration.

    Args:
        storage_type: "file" or "postgres". If None, uses environment configuration.
        **storage_kwargs: Storage-specific configuration parameters

    Returns:
        MonitoringDecorator instance
    """
    if storage_type is None:
        # Use default configuration from environment
        config = StorageConfig()
    else:
        # Create custom configuration
        config = StorageConfig()
        config.storage_type = storage_type

        # Update configuration with provided kwargs
        if storage_type.lower() == "file":
            config.file_base_path = storage_kwargs.get("base_path", config.file_base_path)
        elif storage_type.lower() == "postgres":
            config.postgres_host = storage_kwargs.get("host", config.postgres_host)
            config.postgres_port = storage_kwargs.get("port", config.postgres_port)
            config.postgres_database = storage_kwargs.get("database", config.postgres_database)
            config.postgres_username = storage_kwargs.get("username", config.postgres_username)
            config.postgres_password = storage_kwargs.get("password", config.postgres_password)

    return MonitoringDecorator(config)


# Global instance for use (uses environment configuration)
monitor = MonitoringDecorator()