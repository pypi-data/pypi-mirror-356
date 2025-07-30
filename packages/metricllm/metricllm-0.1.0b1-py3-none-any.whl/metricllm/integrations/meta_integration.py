"""
Meta LLaMA Integration for MetricLLM
===================================

Provides comprehensive integration with Meta's LLaMA models via various providers.
"""

import os
from typing import Dict, Any, List, Optional, Union
from metricllm import monitor

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class MetaIntegration:
    """Meta LLaMA integration with MetricLLM monitoring."""
    
    def __init__(self, api_endpoint: str = None, api_key: str = None):
        """
        Initialize Meta integration.
        Can be used with Hugging Face, Replicate, or other Meta model providers.
        """
        self.api_endpoint = api_endpoint
        self.api_key = api_key or os.getenv("META_API_KEY")
    
    @monitor(provider="meta", model="llama-3.1-405b")
    def chat_llama_3_1_405b(self, prompt: str, **kwargs) -> str:
        """Chat with LLaMA 3.1 405B."""
        # This would typically use a provider like Replicate or Together AI
        if not self.api_endpoint:
            raise ValueError("API endpoint required for Meta models")
        
        response = self._make_request(prompt, "llama-3.1-405b", **kwargs)
        return response
    
    @monitor(provider="meta", model="llama-3.1-70b")
    def chat_llama_3_1_70b(self, prompt: str, **kwargs) -> str:
        """Chat with LLaMA 3.1 70B."""
        if not self.api_endpoint:
            raise ValueError("API endpoint required for Meta models")
        
        response = self._make_request(prompt, "llama-3.1-70b", **kwargs)
        return response
    
    @monitor(provider="meta", model="llama-3.1-8b")
    def chat_llama_3_1_8b(self, prompt: str, **kwargs) -> str:
        """Chat with LLaMA 3.1 8B."""
        if not self.api_endpoint:
            raise ValueError("API endpoint required for Meta models")
        
        response = self._make_request(prompt, "llama-3.1-8b", **kwargs)
        return response
    
    @monitor(provider="meta", model="llama-3-70b")
    def chat_llama_3_70b(self, prompt: str, **kwargs) -> str:
        """Chat with LLaMA 3 70B."""
        if not self.api_endpoint:
            raise ValueError("API endpoint required for Meta models")
        
        response = self._make_request(prompt, "llama-3-70b", **kwargs)
        return response
    
    def _make_request(self, prompt: str, model: str, **kwargs) -> str:
        """Make request to Meta model API."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("Requests package required")
        
        # Generic implementation - would need to be adapted for specific providers
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        
        data = {
            "model": model,
            "prompt": prompt,
            "max_tokens": kwargs.get("max_tokens", 1000),
            "temperature": kwargs.get("temperature", 0.7),
            **kwargs
        }
        
        response = requests.post(self.api_endpoint, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        # This would need to be adapted based on the specific API response format
        return result.get("text", result.get("output", ""))

# Example usage functions for Hugging Face Transformers (local)
@monitor(provider="meta", model="llama-2-7b-chat")
def huggingface_llama_chat(prompt: str) -> str:
    """LLaMA chat via Hugging Face Transformers (requires local installation)."""
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        model_name = "meta-llama/Llama-2-7b-chat-hf"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        inputs = tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=500,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Remove the original prompt from the response
        response = response[len(prompt):].strip()
        
        return response
        
    except ImportError:
        raise ImportError("Transformers and torch packages required for local LLaMA")

@monitor(provider="meta", model="llama-3-8b", custom_metadata={"provider": "together"})
def together_llama_chat(prompt: str) -> str:
    """LLaMA chat via Together AI."""
    if not REQUESTS_AVAILABLE:
        raise ImportError("Requests package required")
    
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY environment variable required")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        json=data,
        headers=headers
    )
    response.raise_for_status()
    
    result = response.json()
    return result["choices"][0]["message"]["content"]

@monitor(provider="meta", model="llama-2-70b", custom_metadata={"provider": "replicate"})
def replicate_llama_chat(prompt: str) -> str:
    """LLaMA chat via Replicate."""
    try:
        import replicate
        
        output = replicate.run(
            "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
            input={
                "prompt": prompt,
                "max_length": 1000,
                "temperature": 0.7
            }
        )
        
        return "".join(output)
        
    except ImportError:
        raise ImportError("Replicate package required: pip install replicate")