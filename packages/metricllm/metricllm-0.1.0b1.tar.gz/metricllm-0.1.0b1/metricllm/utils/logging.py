"""
Logging utilities for MetricLLM.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(name: str, 
                 level: str = "INFO",
                 log_file: Optional[str] = None,
                 format_string: Optional[str] = None,
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5) -> logging.Logger:
    """
    Set up a logger with console and file handlers.
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Path to log file (optional)
        format_string: Custom format string
        max_file_size: Maximum file size before rotation
        backup_count: Number of backup files to keep
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Set level
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Default format
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with default MetricLLM configuration.
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    # Check if logger already exists
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Set up default logger
        log_level = os.getenv("METRICLLM_LOG_LEVEL", "INFO")
        log_file = os.getenv("METRICLLM_LOG_FILE", "logs/metricllm.log")
        
        logger = setup_logger(
            name=name,
            level=log_level,
            log_file=log_file
        )
    
    return logger


class MetricLLMLogger:
    """Enhanced logger for MetricLLM with structured logging support."""
    
    def __init__(self, name: str, context: Optional[dict] = None):
        self.logger = get_logger(name)
        self.context = context or {}
    
    def info(self, message: str, extra: Optional[dict] = None):
        """Log info message with context."""
        self._log(logging.INFO, message, extra)
    
    def debug(self, message: str, extra: Optional[dict] = None):
        """Log debug message with context."""
        self._log(logging.DEBUG, message, extra)
    
    def warning(self, message: str, extra: Optional[dict] = None):
        """Log warning message with context."""
        self._log(logging.WARNING, message, extra)
    
    def error(self, message: str, extra: Optional[dict] = None):
        """Log error message with context."""
        self._log(logging.ERROR, message, extra)
    
    def critical(self, message: str, extra: Optional[dict] = None):
        """Log critical message with context."""
        self._log(logging.CRITICAL, message, extra)
    
    def _log(self, level: int, message: str, extra: Optional[dict] = None):
        """Internal logging method with context merging."""
        # Merge context with extra data
        log_extra = self.context.copy()
        if extra:
            log_extra.update(extra)
        
        # Format message with context if available
        if log_extra:
            context_str = " | ".join([f"{k}={v}" for k, v in log_extra.items()])
            formatted_message = f"{message} | {context_str}"
        else:
            formatted_message = message
        
        self.logger.log(level, formatted_message)
    
    def with_context(self, **kwargs) -> 'MetricLLMLogger':
        """Create a new logger with additional context."""
        new_context = self.context.copy()
        new_context.update(kwargs)
        return MetricLLMLogger(self.logger.name, new_context)


def log_function_call(logger: logging.Logger, func_name: str, args: tuple, kwargs: dict):
    """Log function call details."""
    args_str = ", ".join([str(arg) for arg in args])
    kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
    
    call_details = f"{func_name}("
    if args_str:
        call_details += args_str
    if kwargs_str:
        if args_str:
            call_details += ", "
        call_details += kwargs_str
    call_details += ")"
    
    logger.debug(f"Function call: {call_details}")


def log_performance(logger: logging.Logger, operation: str, duration: float, **metadata):
    """Log performance metrics."""
    metadata_str = " | ".join([f"{k}={v}" for k, v in metadata.items()])
    logger.info(f"Performance: {operation} completed in {duration:.4f}s | {metadata_str}")
