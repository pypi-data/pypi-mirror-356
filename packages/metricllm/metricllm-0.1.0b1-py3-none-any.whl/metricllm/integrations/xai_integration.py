"""
xAI (Grok) Integration for MetricLLM
===================================

Provides comprehensive integration with xAI's Grok API.
"""

import os
from typing import Dict, Any, List, Optional, Union
from metricllm import monitor

try:
    from openai import OpenAI
    XAI_AVAILABLE = True
except ImportError:
    XAI_AVAILABLE = False

class XAIIntegration:
    """xAI Grok API integration with MetricLLM monitoring."""
    
    def __init__(self, api_key: Optional[str] = None):
        if not XAI_AVAILABLE:
            raise ImportError("OpenAI package required for xAI integration. Install with: pip install openai")
        
        # Create a custom OpenAI client with the X.AI endpoint
        self.client = OpenAI(
            base_url="https://api.x.ai/v1", 
            api_key=api_key or os.getenv("XAI_API_KEY")
        )
    
    @monitor(provider="xai", model="grok-2-1212")
    def chat_grok_2(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with Grok-2."""
        response = self.client.chat.completions.create(
            model="grok-2-1212",
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    @monitor(provider="xai", model="grok-2-vision-1212")
    def chat_grok_vision(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        """Chat with Grok Vision."""
        response = self.client.chat.completions.create(
            model="grok-2-vision-1212",
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    @monitor(provider="xai", model="grok-beta")
    def chat_grok_beta(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with Grok Beta."""
        response = self.client.chat.completions.create(
            model="grok-beta",
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

# Example usage functions
@monitor(provider="xai", model="grok-2-1212")
def simple_grok_chat(prompt: str) -> str:
    """Simple Grok chat function with monitoring."""
    if not XAI_AVAILABLE:
        raise ImportError("OpenAI package not available for xAI integration")
    
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=os.getenv("XAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="grok-2-1212",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@monitor(provider="xai", model="grok-2-1212", custom_metadata={"task": "analysis"})
def grok_analysis(prompt: str, system_prompt: str = None) -> str:
    """Analysis using Grok with optional system prompt."""
    if not XAI_AVAILABLE:
        raise ImportError("OpenAI package not available for xAI integration")
    
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=os.getenv("XAI_API_KEY"))
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="grok-2-1212",
        messages=messages
    )
    return response.choices[0].message.content

@monitor(provider="xai", model="grok-2-vision-1212", custom_metadata={"task": "image_analysis"})
def grok_image_analysis(base64_image: str, prompt: str = "Analyze this image") -> str:
    """Image analysis using Grok Vision."""
    if not XAI_AVAILABLE:
        raise ImportError("OpenAI package not available for xAI integration")
    
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=os.getenv("XAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="grok-2-vision-1212",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content