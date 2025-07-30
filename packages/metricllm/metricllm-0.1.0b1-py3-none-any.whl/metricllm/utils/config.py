"""
Configuration management for MetricLLM.
"""

import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

from metricllm.utils.logging import get_logger


@dataclass
class MonitoringConfig:
    """Configuration for monitoring features."""
    track_tokens: bool = True
    track_cost: bool = True
    evaluate: bool = True
    responsible_ai_check: bool = True
    log_level: str = "INFO"
    storage_path: str = "data"
    auto_export: bool = False
    export_interval_hours: int = 24


@dataclass
class LoggingConfig:
    """Configuration for logging."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "logs/metricllm.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


@dataclass
class StorageConfig:
    """Configuration for storage."""
    base_path: str = "data"
    enable_daily_files: bool = True
    enable_compression: bool = False
    retention_days: int = 30
    auto_cleanup: bool = False


@dataclass
class EvaluationConfig:
    """Configuration for evaluation framework."""
    enabled_evaluators: list = None
    custom_evaluators: dict = None
    evaluation_threshold: float = 2.5
    auto_flag_low_scores: bool = True
    
    def __post_init__(self):
        if self.enabled_evaluators is None:
            self.enabled_evaluators = [
                "basic_quality", "coherence", "relevance", 
                "completeness", "factual_consistency", "linguistic_quality"
            ]
        if self.custom_evaluators is None:
            self.custom_evaluators = {}


@dataclass
class ResponsibleAIConfig:
    """Configuration for responsible AI checks."""
    content_filtering: bool = True
    bias_detection: bool = True
    toxicity_analysis: bool = True
    privacy_check: bool = True
    fairness_assessment: bool = True
    safety_threshold: float = 0.6
    auto_flag_unsafe: bool = True
    custom_keywords: dict = None
    
    def __post_init__(self):
        if self.custom_keywords is None:
            self.custom_keywords = {}


class Config:
    """Main configuration class for MetricLLM."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.logger = get_logger(__name__)
        self.config_file = config_file or os.path.join(os.getcwd(), "metricllm_config.json")
        
        # Initialize default configurations
        self.monitoring = MonitoringConfig()
        self.logging = LoggingConfig()
        self.storage = StorageConfig()
        self.evaluation = EvaluationConfig()
        self.responsible_ai = ResponsibleAIConfig()
        
        # Load configuration from file if it exists
        self.load_config()
        
        # Override with environment variables if present
        self.load_from_env()
    
    def load_config(self):
        """Load configuration from JSON file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Update configurations
                if "monitoring" in config_data:
                    self._update_config(self.monitoring, config_data["monitoring"])
                
                if "logging" in config_data:
                    self._update_config(self.logging, config_data["logging"])
                
                if "storage" in config_data:
                    self._update_config(self.storage, config_data["storage"])
                
                if "evaluation" in config_data:
                    self._update_config(self.evaluation, config_data["evaluation"])
                
                if "responsible_ai" in config_data:
                    self._update_config(self.responsible_ai, config_data["responsible_ai"])
                
                self.logger.info(f"Configuration loaded from {self.config_file}")
            
        except Exception as e:
            self.logger.warning(f"Failed to load configuration: {str(e)}")
    
    def save_config(self):
        """Save current configuration to JSON file."""
        try:
            config_data = {
                "monitoring": asdict(self.monitoring),
                "logging": asdict(self.logging),
                "storage": asdict(self.storage),
                "evaluation": asdict(self.evaluation),
                "responsible_ai": asdict(self.responsible_ai)
            }
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configuration saved to {self.config_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {str(e)}")
    
    def load_from_env(self):
        """Load configuration from environment variables."""
        # Monitoring configuration
        self.monitoring.track_tokens = self._get_env_bool("METRICLLM_TRACK_TOKENS", self.monitoring.track_tokens)
        self.monitoring.track_cost = self._get_env_bool("METRICLLM_TRACK_COST", self.monitoring.track_cost)
        self.monitoring.evaluate = self._get_env_bool("METRICLLM_EVALUATE", self.monitoring.evaluate)
        self.monitoring.responsible_ai_check = self._get_env_bool("METRICLLM_RESPONSIBLE_AI", self.monitoring.responsible_ai_check)
        self.monitoring.log_level = os.getenv("METRICLLM_LOG_LEVEL", self.monitoring.log_level)
        self.monitoring.storage_path = os.getenv("METRICLLM_STORAGE_PATH", self.monitoring.storage_path)
        
        # Logging configuration
        self.logging.level = os.getenv("METRICLLM_LOGGING_LEVEL", self.logging.level)
        self.logging.file_path = os.getenv("METRICLLM_LOG_FILE", self.logging.file_path)
        
        # Storage configuration
        self.storage.base_path = os.getenv("METRICLLM_DATA_PATH", self.storage.base_path)
        self.storage.retention_days = int(os.getenv("METRICLLM_RETENTION_DAYS", str(self.storage.retention_days)))
        
        # Responsible AI configuration
        self.responsible_ai.safety_threshold = float(os.getenv("METRICLLM_SAFETY_THRESHOLD", str(self.responsible_ai.safety_threshold)))
    
    def get_monitor_config(self) -> Dict[str, Any]:
        """Get configuration for the monitor decorator."""
        return {
            "track_tokens": self.monitoring.track_tokens,
            "track_cost": self.monitoring.track_cost,
            "evaluate": self.monitoring.evaluate,
            "responsible_ai_check": self.monitoring.responsible_ai_check,
            "log_level": self.monitoring.log_level
        }
    
    def update_config(self, section: str, config_dict: Dict[str, Any]):
        """Update a configuration section."""
        if section == "monitoring":
            self._update_config(self.monitoring, config_dict)
        elif section == "logging":
            self._update_config(self.logging, config_dict)
        elif section == "storage":
            self._update_config(self.storage, config_dict)
        elif section == "evaluation":
            self._update_config(self.evaluation, config_dict)
        elif section == "responsible_ai":
            self._update_config(self.responsible_ai, config_dict)
        else:
            raise ValueError(f"Unknown configuration section: {section}")
    
    def _update_config(self, config_obj, config_dict: Dict[str, Any]):
        """Update a configuration object with values from dictionary."""
        for key, value in config_dict.items():
            if hasattr(config_obj, key):
                setattr(config_obj, key, value)
    
    def _get_env_bool(self, env_var: str, default: bool) -> bool:
        """Get boolean value from environment variable."""
        value = os.getenv(env_var, "").lower()
        if value in ("true", "1", "yes", "on"):
            return True
        elif value in ("false", "0", "no", "off"):
            return False
        else:
            return default
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as dictionary."""
        return {
            "monitoring": asdict(self.monitoring),
            "logging": asdict(self.logging),
            "storage": asdict(self.storage),
            "evaluation": asdict(self.evaluation),
            "responsible_ai": asdict(self.responsible_ai)
        }
