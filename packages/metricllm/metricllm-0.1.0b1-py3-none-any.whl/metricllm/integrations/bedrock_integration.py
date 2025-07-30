"""
Amazon Bedrock Integration for MetricLLM
========================================

Provides comprehensive integration with Amazon Bedrock LLM models.
"""

import os
import json
from typing import Dict, Any, List, Optional, Union
from metricllm import monitor

try:
    import boto3
    BEDROCK_AVAILABLE = True
except ImportError:
    BEDROCK_AVAILABLE = False

class BedrockIntegration:
    """Amazon Bedrock integration with MetricLLM monitoring."""
    
    def __init__(self, region_name: str = "us-east-1", **kwargs):
        if not BEDROCK_AVAILABLE:
            raise ImportError("Boto3 package not installed. Install with: pip install boto3")
        
        self.region_name = region_name
        self.bedrock = boto3.client('bedrock-runtime', region_name=region_name, **kwargs)
    
    def _invoke_model(self, model_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke a Bedrock model."""
        response = self.bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType='application/json',
            accept='application/json'
        )
        return json.loads(response['body'].read())
    
    @monitor(provider="amazon", model="claude-3-sonnet-bedrock")
    def chat_claude_bedrock(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with Claude via Bedrock."""
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": kwargs.get("max_tokens", 1000),
            "messages": messages,
            **{k: v for k, v in kwargs.items() if k != "max_tokens"}
        }
        
        response = self._invoke_model("anthropic.claude-3-sonnet-20240229-v1:0", body)
        return response["content"][0]["text"]
    
    @monitor(provider="amazon", model="titan-text-express")
    def chat_titan_express(self, prompt: str, **kwargs) -> str:
        """Chat with Amazon Titan Text Express."""
        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.7),
                "topP": kwargs.get("top_p", 0.9),
                **{k: v for k, v in kwargs.items() if k not in ["max_tokens", "temperature", "top_p"]}
            }
        }
        
        response = self._invoke_model("amazon.titan-text-express-v1", body)
        return response["results"][0]["outputText"]
    
    @monitor(provider="amazon", model="meta-llama2-70b")
    def chat_llama2_bedrock(self, prompt: str, **kwargs) -> str:
        """Chat with Llama 2 via Bedrock."""
        body = {
            "prompt": prompt,
            "max_gen_len": kwargs.get("max_tokens", 1000),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
            **{k: v for k, v in kwargs.items() if k not in ["max_tokens", "temperature", "top_p"]}
        }
        
        response = self._invoke_model("meta.llama2-70b-chat-v1", body)
        return response["generation"]
    
    @monitor(provider="amazon", model="cohere-command")
    def chat_cohere_bedrock(self, prompt: str, **kwargs) -> str:
        """Chat with Cohere Command via Bedrock."""
        body = {
            "prompt": prompt,
            "max_tokens": kwargs.get("max_tokens", 1000),
            "temperature": kwargs.get("temperature", 0.7),
            "p": kwargs.get("top_p", 0.9),
            **{k: v for k, v in kwargs.items() if k not in ["max_tokens", "temperature", "top_p"]}
        }
        
        response = self._invoke_model("cohere.command-text-v14", body)
        return response["generations"][0]["text"]

# Example usage functions
@monitor(provider="amazon", model="claude-3-sonnet-bedrock")
def simple_bedrock_claude(prompt: str) -> str:
    """Simple Claude via Bedrock with monitoring."""
    if not BEDROCK_AVAILABLE:
        raise ImportError("Boto3 package not available")
    
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body),
        contentType='application/json',
        accept='application/json'
    )
    
    result = json.loads(response['body'].read())
    return result["content"][0]["text"]

@monitor(provider="amazon", model="titan-text-express", custom_metadata={"task": "generation"})
def bedrock_text_generation(prompt: str, max_tokens: int = 500) -> str:
    """Text generation with Amazon Titan."""
    if not BEDROCK_AVAILABLE:
        raise ImportError("Boto3 package not available")
    
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": max_tokens,
            "temperature": 0.7,
            "topP": 0.9
        }
    }
    
    response = bedrock.invoke_model(
        modelId="amazon.titan-text-express-v1",
        body=json.dumps(body),
        contentType='application/json',
        accept='application/json'
    )
    
    result = json.loads(response['body'].read())
    return result["results"][0]["outputText"]

@monitor(provider="amazon", model="meta-llama2-70b", custom_metadata={"task": "conversation"})
def bedrock_llama_conversation(prompt: str, temperature: float = 0.7) -> str:
    """Conversation with Llama 2 via Bedrock."""
    if not BEDROCK_AVAILABLE:
        raise ImportError("Boto3 package not available")
    
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    body = {
        "prompt": prompt,
        "max_gen_len": 1000,
        "temperature": temperature,
        "top_p": 0.9
    }
    
    response = bedrock.invoke_model(
        modelId="meta.llama2-70b-chat-v1",
        body=json.dumps(body),
        contentType='application/json',
        accept='application/json'
    )
    
    result = json.loads(response['body'].read())
    return result["generation"]