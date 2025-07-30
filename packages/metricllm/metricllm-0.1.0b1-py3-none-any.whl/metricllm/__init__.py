"""
MetricLLM - Comprehensive LLM Monitoring Package
===============================================

An open-source Python package for monitoring Large Language Models with
decorator-based integration and comprehensive analytics.
"""

from metricllm.core.monitor import monitor
from metricllm.prompts.manager import PromptManager
from metricllm.storage.file_store import FileStore
from metricllm.utils.config import Config

__version__ = "0.1.0"
__author__ = "MetricLLM Team"

# Main exports
__all__ = [
    "monitor",
    "PromptManager",
    "FileStore",
    "Config"
]

# Initialize default configuration
_config = Config()
_prompt_manager = PromptManager()
_file_store = FileStore()


def get_config():
    """Get the global configuration instance."""
    return _config


def get_prompt_manager():
    """Get the global prompt manager instance."""
    return _prompt_manager


def get_file_store():
    """Get the global file store instance."""
    return _file_store
