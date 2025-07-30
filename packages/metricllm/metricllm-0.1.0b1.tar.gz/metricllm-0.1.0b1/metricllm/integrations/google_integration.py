"""
Google AI Integration for MetricLLM
==================================

Provides comprehensive integration with Google's Gemini and PaLM APIs.
"""

import os
from typing import Dict, Any, List, Optional, Union
from metricllm import monitor

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

class GoogleIntegration:
    """Google AI integration with MetricLLM monitoring."""
    
    def __init__(self, api_key: Optional[str] = None):
        if not GOOGLE_AVAILABLE:
            raise ImportError("Google AI package not installed. Install with: pip install google-generativeai")
        
        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
    
    @monitor(provider="google", model="gemini-1.5-pro")
    def chat_gemini_pro_15(self, prompt: str, **kwargs) -> str:
        """Chat with Gemini 1.5 Pro."""
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt, **kwargs)
        return response.text
    
    @monitor(provider="google", model="gemini-1.5-flash")
    def chat_gemini_flash_15(self, prompt: str, **kwargs) -> str:
        """Chat with Gemini 1.5 Flash."""
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt, **kwargs)
        return response.text
    
    @monitor(provider="google", model="gemini-pro")
    def chat_gemini_pro(self, prompt: str, **kwargs) -> str:
        """Chat with Gemini Pro."""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt, **kwargs)
        return response.text
    
    @monitor(provider="google", model="gemini-pro-vision")
    def analyze_image_gemini(self, prompt: str, image_data: bytes, **kwargs) -> str:
        """Analyze image with Gemini Pro Vision."""
        model = genai.GenerativeModel('gemini-pro-vision')
        image_part = {
            "mime_type": "image/jpeg",
            "data": image_data
        }
        response = model.generate_content([prompt, image_part], **kwargs)
        return response.text

# Example usage functions
@monitor(provider="google", model="gemini-1.5-pro")
def simple_gemini_chat(prompt: str) -> str:
    """Simple Gemini chat function with monitoring."""
    if not GOOGLE_AVAILABLE:
        raise ImportError("Google AI package not available")
    
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    return response.text

@monitor(provider="google", model="gemini-1.5-flash", custom_metadata={"task": "quick_response"})
def gemini_quick_response(prompt: str) -> str:
    """Quick response using Gemini Flash."""
    if not GOOGLE_AVAILABLE:
        raise ImportError("Google AI package not available")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

@monitor(provider="google", model="gemini-pro", custom_metadata={"task": "structured_data"})
def gemini_structured_analysis(data: str, analysis_type: str) -> str:
    """Structured data analysis with Gemini."""
    if not GOOGLE_AVAILABLE:
        raise ImportError("Google AI package not available")
    
    prompt = f"Perform {analysis_type} analysis on the following data:\n\n{data}"
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

@monitor(provider="google", model="gemini-1.5-pro", custom_metadata={"task": "conversation"})
def gemini_conversation(messages: List[Dict[str, str]]) -> str:
    """Multi-turn conversation with Gemini."""
    if not GOOGLE_AVAILABLE:
        raise ImportError("Google AI package not available")
    
    model = genai.GenerativeModel('gemini-1.5-pro')
    chat = model.start_chat(history=[])
    
    # Add conversation history
    for message in messages[:-1]:
        if message["role"] == "user":
            chat.send_message(message["content"])
    
    # Send final message and get response
    response = chat.send_message(messages[-1]["content"])
    return response.text