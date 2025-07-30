"""
OpenAI Integration for MetricLLM
===============================

Provides comprehensive integration with OpenAI's API including GPT-4, GPT-3.5, and other models.
"""

import os
from typing import Dict, Any, List, Optional, Union
from metricllm import monitor

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class OpenAIIntegration:
    """OpenAI API integration with MetricLLM monitoring."""
    
    def __init__(self, api_key: Optional[str] = None):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Install with: pip install openai")
        
        self.client = openai.OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
    
    @monitor(provider="openai", model="gpt-4")
    def chat_completion_gpt4(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat completion using GPT-4."""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    @monitor(provider="openai", model="gpt-4-turbo")
    def chat_completion_gpt4_turbo(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat completion using GPT-4 Turbo."""
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    @monitor(provider="openai", model="gpt-4o")
    def chat_completion_gpt4o(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat completion using GPT-4o."""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    @monitor(provider="openai", model="gpt-3.5-turbo")
    def chat_completion_gpt35(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat completion using GPT-3.5 Turbo."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    @monitor(provider="openai", model="gpt-3.5-turbo-instruct")
    def completion_gpt35_instruct(self, prompt: str, **kwargs) -> str:
        """Text completion using GPT-3.5 Turbo Instruct."""
        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            **kwargs
        )
        return response.choices[0].text
    
    @monitor(provider="openai", model="text-embedding-3-large")
    def create_embeddings(self, text: Union[str, List[str]], **kwargs) -> List[float]:
        """Create embeddings using OpenAI's embedding model."""
        response = self.client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            **kwargs
        )
        if isinstance(text, str):
            return response.data[0].embedding
        return [item.embedding for item in response.data]

# Example usage functions
@monitor(provider="openai", model="gpt-4")
def simple_openai_chat(prompt: str, model: str = "gpt-4") -> str:
    """Simple OpenAI chat function with monitoring."""
    if not OPENAI_AVAILABLE:
        raise ImportError("OpenAI package not available")
    
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@monitor(provider="openai", model="gpt-3.5-turbo")
def openai_conversation(messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
    """OpenAI conversation with full response monitoring."""
    if not OPENAI_AVAILABLE:
        raise ImportError("OpenAI package not available")
    
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature
    )
    return response

@monitor(provider="openai", model="gpt-4", custom_metadata={"task": "code_generation"})
def openai_code_assistant(prompt: str, language: str = "python") -> str:
    """Code generation assistant with OpenAI."""
    if not OPENAI_AVAILABLE:
        raise ImportError("OpenAI package not available")
    
    system_prompt = f"You are an expert {language} programmer. Generate clean, efficient, and well-documented code."
    
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

@monitor(provider="openai", model="gpt-4o", custom_metadata={"task": "vision"})
def openai_vision_analysis(image_url: str, prompt: str = "Describe this image") -> str:
    """Image analysis using GPT-4 Vision."""
    if not OPENAI_AVAILABLE:
        raise ImportError("OpenAI package not available")
    
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content