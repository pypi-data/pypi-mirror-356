"""
Ollama Integration for MetricLLM
===============================

Provides comprehensive integration with Ollama local LLM models.
"""

import os
import requests
from typing import Dict, Any, List, Optional, Union
from metricllm import monitor

class OllamaIntegration:
    """Ollama local LLM integration with MetricLLM monitoring."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request to Ollama API."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    @monitor(provider="ollama", model="llama3")
    def chat_llama3(self, prompt: str, **kwargs) -> str:
        """Chat with Llama 3 via Ollama."""
        data = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        response = self._make_request("api/generate", data)
        return response.get("response", "")
    
    @monitor(provider="ollama", model="llama2")
    def chat_llama2(self, prompt: str, **kwargs) -> str:
        """Chat with Llama 2 via Ollama."""
        data = {
            "model": "llama2",
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        response = self._make_request("api/generate", data)
        return response.get("response", "")
    
    @monitor(provider="ollama", model="mistral")
    def chat_mistral(self, prompt: str, **kwargs) -> str:
        """Chat with Mistral via Ollama."""
        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        response = self._make_request("api/generate", data)
        return response.get("response", "")
    
    @monitor(provider="ollama", model="codellama")
    def code_generation(self, prompt: str, **kwargs) -> str:
        """Code generation with Code Llama via Ollama."""
        data = {
            "model": "codellama",
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        response = self._make_request("api/generate", data)
        return response.get("response", "")

# Example usage functions
@monitor(provider="ollama", model="llama3")
def simple_ollama_chat(prompt: str, model: str = "llama3") -> str:
    """Simple Ollama chat function with monitoring."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ollama server not available: {str(e)}")

@monitor(provider="ollama", model="llama3", custom_metadata={"task": "conversation"})
def ollama_conversation(messages: List[Dict[str, str]], model: str = "llama3") -> str:
    """Multi-turn conversation with Ollama."""
    # Convert messages to a single prompt
    conversation_text = ""
    for message in messages:
        role = message.get("role", "user")
        content = message.get("content", "")
        conversation_text += f"{role.capitalize()}: {content}\n"
    
    conversation_text += "Assistant: "
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": conversation_text,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ollama server not available: {str(e)}")

@monitor(provider="ollama", model="codellama", custom_metadata={"task": "code_generation"})
def ollama_code_assistant(prompt: str, language: str = "python") -> str:
    """Code generation with Ollama Code Llama."""
    code_prompt = f"Generate {language} code for the following request:\n\n{prompt}\n\nCode:"
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "codellama",
                "prompt": code_prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ollama server not available: {str(e)}")

@monitor(provider="ollama", model="mistral", custom_metadata={"task": "analysis"})
def ollama_text_analysis(text: str, analysis_type: str = "summary") -> str:
    """Text analysis using Ollama Mistral."""
    analysis_prompt = f"Perform {analysis_type} analysis on the following text:\n\n{text}"
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": analysis_prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ollama server not available: {str(e)}")

@monitor(provider="ollama", model="phi", custom_metadata={"task": "quick_response"})
def ollama_quick_response(prompt: str) -> str:
    """Quick response using lightweight Phi model."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 100}  # Limit response length for quick responses
            }
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ollama server not available: {str(e)}")