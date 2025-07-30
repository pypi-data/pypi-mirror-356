"""
Trace logging for LLM interactions.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional

from metricllm.utils.logging import get_logger


class TraceLogger:
    """Logs detailed traces of LLM interactions."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def log_trace(self,
                  trace_id: str,
                  function_name: str,
                  provider: str,
                  model: str,
                  prompt_data: Dict[str, Any],
                  response_data: Dict[str, Any],
                  metrics: Dict[str, Any],
                  execution_time: float,
                  custom_metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Log a comprehensive trace of an LLM interaction.
        
        Args:
            trace_id: Unique identifier for this trace
            function_name: Name of the function being monitored
            provider: LLM provider
            model: Model name
            prompt_data: Input prompt and parameters
            response_data: Response data
            metrics: Collected metrics
            execution_time: Execution time
            custom_metadata: Additional metadata
        
        Returns:
            Trace data dictionary
        """
        trace_data = {"trace_id": trace_id, "timestamp": datetime.now().isoformat(), "function_name": function_name,
                      "provider": provider, "model": model, "execution_time": execution_time,
                      "input": self._sanitize_input_data(prompt_data),
                      "output": self._sanitize_output_data(response_data), "metrics": metrics,
                      "metadata": custom_metadata or {}, "trace_version": "1.0", "span": {
                "span_id": trace_id,
                "parent_span_id": None,  # Could be extended for nested calls
                "operation_name": f"llm_call_{provider}_{model}",
                "start_time": datetime.now().isoformat(),
                "duration_ms": round(execution_time * 1000, 2),
                "tags": {
                    "llm.provider": provider,
                    "llm.model": model,
                    "llm.function": function_name,
                    "llm.prompt_tokens": metrics.get("prompt_tokens", 0),
                    "llm.completion_tokens": metrics.get("completion_tokens", 0),
                    "llm.total_tokens": metrics.get("total_tokens", 0)
                }
            }}
        
        # Add span information for distributed tracing

        # Log the trace
        self.logger.info(f"Trace logged: {trace_id}", extra={"trace_data": trace_data})
        
        return trace_data
    
    def _sanitize_input_data(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize input data for logging."""
        sanitized = {}
        
        for key, value in prompt_data.items():
            if key == "prompt":
                # Truncate very long prompts
                if isinstance(value, str) and len(value) > 10000:
                    sanitized[key] = value[:10000] + "... [truncated]"
                else:
                    sanitized[key] = value
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _sanitize_output_data(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize output data for logging."""
        sanitized = {}
        
        for key, value in response_data.items():
            if key == "response":
                # Truncate very long responses
                if isinstance(value, str) and len(value) > 10000:
                    sanitized[key] = value[:10000] + "... [truncated]"
                else:
                    sanitized[key] = value
            else:
                sanitized[key] = value
        
        return sanitized
    
    def create_trace_summary(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of the trace for quick overview."""
        return {
            "trace_id": trace_data["trace_id"],
            "timestamp": trace_data["timestamp"],
            "provider": trace_data["provider"],
            "model": trace_data["model"],
            "function": trace_data["function_name"],
            "execution_time": trace_data["execution_time"],
            "status": "success",
            "prompt_length": len(trace_data["input"].get("prompt", "")),
            "response_length": len(trace_data["output"].get("response", "")),
            "total_tokens": trace_data["metrics"].get("total_tokens", 0),
            "estimated_cost": trace_data["metrics"].get("estimated_cost_usd", 0.0)
        }
