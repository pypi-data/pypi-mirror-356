"""
Metrics collection for LLM monitoring.
"""

import time
from datetime import datetime
from typing import Dict, Any, Optional

from metricllm.utils.logging import get_logger


class MetricsCollector:
    """Collects various metrics for LLM interactions."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Token pricing per 1K tokens (approximate as of 2024)
        self.pricing = {
            "openai": {
                "gpt-4": {"input": 0.03, "output": 0.06},
                "gpt-4-turbo": {"input": 0.01, "output": 0.03},
                "gpt-4o": {"input": 0.005, "output": 0.015},
                "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
                "gpt-3.5-turbo-instruct": {"input": 0.0015, "output": 0.002},
            },
            "anthropic": {
                "claude-3-opus": {"input": 0.015, "output": 0.075},
                "claude-3-5-sonnet": {"input": 0.003, "output": 0.015},
                "claude-3-sonnet": {"input": 0.003, "output": 0.015},
                "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
                "claude-3-5-haiku": {"input": 0.001, "output": 0.005},
            },
            "google": {
                "gemini-pro": {"input": 0.0005, "output": 0.0015},
                "gemini-pro-vision": {"input": 0.0005, "output": 0.0015},
                "gemini-1.5-pro": {"input": 0.003, "output": 0.015},
                "gemini-1.5-flash": {"input": 0.00015, "output": 0.0006},
                "text-bison": {"input": 0.001, "output": 0.001},
                "chat-bison": {"input": 0.0005, "output": 0.0005},
            },
            "amazon": {
                "claude-3-opus-bedrock": {"input": 0.015, "output": 0.075},
                "claude-3-sonnet-bedrock": {"input": 0.003, "output": 0.015},
                "claude-3-haiku-bedrock": {"input": 0.00025, "output": 0.00125},
                "titan-text-express": {"input": 0.0008, "output": 0.0016},
                "titan-text-lite": {"input": 0.0003, "output": 0.0004},
                "cohere-command": {"input": 0.0015, "output": 0.002},
                "ai21-j2-ultra": {"input": 0.0125, "output": 0.0125},
                "meta-llama2-70b": {"input": 0.00195, "output": 0.00256},
            },
            "xai": {
                "grok-beta": {"input": 0.005, "output": 0.015},
                "grok-vision-beta": {"input": 0.005, "output": 0.015},
                "grok-2-1212": {"input": 0.002, "output": 0.01},
                "grok-2-vision-1212": {"input": 0.002, "output": 0.01},
            },
            "meta": {
                "llama-2-7b": {"input": 0.0002, "output": 0.0002},
                "llama-2-13b": {"input": 0.0003, "output": 0.0004},
                "llama-2-70b": {"input": 0.0009, "output": 0.0009},
                "llama-3-8b": {"input": 0.00015, "output": 0.00015},
                "llama-3-70b": {"input": 0.0008, "output": 0.0008},
                "llama-3.1-8b": {"input": 0.00015, "output": 0.00015},
                "llama-3.1-70b": {"input": 0.0008, "output": 0.0008},
                "llama-3.1-405b": {"input": 0.005, "output": 0.005},
            },
            "ollama": {
                # Ollama is typically local/free, but we can estimate compute costs
                "llama2": {"input": 0.0, "output": 0.0},
                "llama3": {"input": 0.0, "output": 0.0},
                "mistral": {"input": 0.0, "output": 0.0},
                "codellama": {"input": 0.0, "output": 0.0},
                "phi": {"input": 0.0, "output": 0.0},
                "vicuna": {"input": 0.0, "output": 0.0},
            },
            "huggingface": {
                "llama-2-7b-chat": {"input": 0.0002, "output": 0.0002},
                "llama-2-13b-chat": {"input": 0.0003, "output": 0.0004},
                "llama-2-70b-chat": {"input": 0.0009, "output": 0.0009},
                "mistral-7b": {"input": 0.0002, "output": 0.0002},
                "mixtral-8x7b": {"input": 0.0007, "output": 0.0007},
            }
        }
    
    def collect(self, 
                provider: str,
                model: str,
                prompt: str,
                response: str,
                execution_time: float,
                track_tokens: bool = True,
                track_cost: bool = True,
                usage_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Collect comprehensive metrics for an LLM interaction.
        
        Args:
            provider: LLM provider name
            model: Model name
            prompt: Input prompt
            response: Model response
            execution_time: Time taken for the call
            track_tokens: Whether to track token usage
            track_cost: Whether to estimate costs
            usage_data: Actual usage data from the API response
        
        Returns:
            Dictionary containing collected metrics
        """
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "model": model,
            "execution_time_seconds": round(execution_time, 4),
            "execution_time_ms": round(execution_time * 1000, 2)
        }
        
        # Basic text metrics
        metrics.update(self._calculate_text_metrics(prompt, response))
        
        # Token metrics
        if track_tokens:
            token_metrics = self._calculate_token_metrics(prompt, response, usage_data)
            metrics.update(token_metrics)
        
        # Cost estimation
        if track_cost and track_tokens:
            cost_metrics = self._estimate_costs(
                provider, model, 
                metrics.get("prompt_tokens", 0),
                metrics.get("completion_tokens", 0)
            )
            metrics.update(cost_metrics)
        
        # Performance metrics
        metrics.update(self._calculate_performance_metrics(execution_time, metrics))
        
        return metrics
    
    def _calculate_text_metrics(self, prompt: str, response: str) -> Dict[str, Any]:
        """Calculate basic text-based metrics."""
        return {
            "prompt_length": len(prompt),
            "response_length": len(response),
            "prompt_words": len(prompt.split()),
            "response_words": len(response.split()),
            "prompt_lines": len(prompt.split('\n')),
            "response_lines": len(response.split('\n'))
        }
    
    def _calculate_token_metrics(self, prompt: str, response: str, usage_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Calculate token-based metrics."""
        if usage_data:
            # Use actual usage data if available
            return {
                "prompt_tokens": usage_data.get("prompt_tokens", 0),
                "completion_tokens": usage_data.get("completion_tokens", 0),
                "total_tokens": usage_data.get("total_tokens", 0)
            }
        else:
            # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
            prompt_tokens = max(1, len(prompt) // 4)
            completion_tokens = max(1, len(response) // 4)
            
            return {
                "prompt_tokens_estimated": prompt_tokens,
                "completion_tokens_estimated": completion_tokens,
                "total_tokens_estimated": prompt_tokens + completion_tokens
            }
    
    def _estimate_costs(self, provider: str, model: str, prompt_tokens: int, completion_tokens: int) -> Dict[str, Any]:
        """Estimate costs based on token usage."""
        cost_data = {
            "estimated_cost_usd": 0.0,
            "cost_breakdown": {
                "input_cost": 0.0,
                "output_cost": 0.0
            },
            "pricing_source": "estimated"
        }
        
        if provider.lower() in self.pricing:
            provider_pricing = self.pricing[provider.lower()]
            
            # Find the closest matching model
            model_key = None
            for key in provider_pricing.keys():
                if key.lower() in model.lower():
                    model_key = key
                    break
            
            if model_key:
                pricing = provider_pricing[model_key]
                
                # Calculate costs (pricing is per 1K tokens)
                input_cost = (prompt_tokens / 1000) * pricing["input"]
                output_cost = (completion_tokens / 1000) * pricing["output"]
                
                cost_data.update({
                    "estimated_cost_usd": round(input_cost + output_cost, 6),
                    "cost_breakdown": {
                        "input_cost": round(input_cost, 6),
                        "output_cost": round(output_cost, 6)
                    },
                    "pricing_model": model_key,
                    "pricing_per_1k_tokens": pricing
                })
        
        return cost_data
    
    def _calculate_performance_metrics(self, execution_time: float, metrics: Dict) -> Dict[str, Any]:
        """Calculate performance-related metrics."""
        performance_metrics = {}
        
        # Tokens per second
        total_tokens = metrics.get("total_tokens", metrics.get("total_tokens_estimated", 0))
        if total_tokens > 0 and execution_time > 0:
            performance_metrics["tokens_per_second"] = round(total_tokens / execution_time, 2)
        
        # Response generation speed (characters per second)
        response_length = metrics.get("response_length", 0)
        if response_length > 0 and execution_time > 0:
            performance_metrics["chars_per_second"] = round(response_length / execution_time, 2)
        
        # Categorize response time
        if execution_time < 1:
            performance_metrics["response_time_category"] = "fast"
        elif execution_time < 5:
            performance_metrics["response_time_category"] = "medium"
        else:
            performance_metrics["response_time_category"] = "slow"
        
        return performance_metrics
