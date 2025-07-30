"""
Anthropic Integration for MetricLLM
==================================

Provides comprehensive integration with Anthropic's Claude API.
"""

import os
from typing import Dict, Any, List, Optional, Union
from metricllm import monitor

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

class AnthropicIntegration:
    """Anthropic Claude API integration with MetricLLM monitoring."""
    
    def __init__(self, api_key: Optional[str] = None):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic package not installed. Install with: pip install anthropic")
        
        # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
        self.client = anthropic.Anthropic(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY")
        )
    
    @monitor(provider="anthropic", model="claude-3-5-sonnet-20241022")
    def chat_claude_3_5_sonnet(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with Claude 3.5 Sonnet."""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=messages,
            max_tokens=kwargs.get("max_tokens", 1000),
            **{k: v for k, v in kwargs.items() if k != "max_tokens"}
        )
        return response.content[0].text
    
    @monitor(provider="anthropic", model="claude-3-opus-20240229")
    def chat_claude_3_opus(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with Claude 3 Opus."""
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            messages=messages,
            max_tokens=kwargs.get("max_tokens", 1000),
            **{k: v for k, v in kwargs.items() if k != "max_tokens"}
        )
        return response.content[0].text
    
    @monitor(provider="anthropic", model="claude-3-sonnet-20240229")
    def chat_claude_3_sonnet(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with Claude 3 Sonnet."""
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=messages,
            max_tokens=kwargs.get("max_tokens", 1000),
            **{k: v for k, v in kwargs.items() if k != "max_tokens"}
        )
        return response.content[0].text
    
    @monitor(provider="anthropic", model="claude-3-haiku-20240307")
    def chat_claude_3_haiku(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with Claude 3 Haiku."""
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            messages=messages,
            max_tokens=kwargs.get("max_tokens", 1000),
            **{k: v for k, v in kwargs.items() if k != "max_tokens"}
        )
        return response.content[0].text

# Example usage functions
@monitor(provider="anthropic", model="claude-3-5-sonnet-20241022")
def simple_claude_chat(prompt: str, max_tokens: int = 1000) -> str:
    """Simple Claude chat function with monitoring."""
    if not ANTHROPIC_AVAILABLE:
        raise ImportError("Anthropic package not available")
    
    # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

@monitor(provider="anthropic", model="claude-3-opus-20240229")
def claude_analysis(prompt: str, system_prompt: str = None) -> str:
    """Claude analysis with system prompt."""
    if not ANTHROPIC_AVAILABLE:
        raise ImportError("Anthropic package not available")
    
    client = anthropic.Anthropic()
    
    messages = [{"role": "user", "content": prompt}]
    
    kwargs = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 2000,
        "messages": messages
    }
    
    if system_prompt:
        kwargs["system"] = system_prompt
    
    response = client.messages.create(**kwargs)
    return response.content[0].text

@monitor(provider="anthropic", model="claude-3-5-sonnet-20241022", custom_metadata={"task": "code_review"})
def claude_code_review(code: str, language: str = "python") -> str:
    """Code review using Claude."""
    if not ANTHROPIC_AVAILABLE:
        raise ImportError("Anthropic package not available")
    
    system_prompt = f"You are an expert {language} code reviewer. Provide detailed feedback on code quality, best practices, potential bugs, and suggestions for improvement."
    
    prompt = f"Please review this {language} code:\n\n```{language}\n{code}\n```"
    
    # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

@monitor(provider="anthropic", model="claude-3-haiku-20240307", custom_metadata={"task": "summarization"})
def claude_quick_summary(text: str, max_sentences: int = 3) -> str:
    """Quick text summarization using Claude Haiku."""
    if not ANTHROPIC_AVAILABLE:
        raise ImportError("Anthropic package not available")
    
    prompt = f"Summarize the following text in {max_sentences} sentences or less:\n\n{text}"
    
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text