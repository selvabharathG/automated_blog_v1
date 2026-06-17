"""
Module: Config Manager
Purpose: Centralized configuration management for all environments
Author: Research Team
"""

import os
import yaml
from typing import Dict, Any, Optional, List
from dotenv import dotenv_values
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ConfigManager:
    """Manages YAML configs and environment variables"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, config_dir: str = "config"):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.config_dir = config_dir
        self._config_cache: Dict[str, Any] = {}
        self._env_cache: Dict[str, str] = {}
        
        try:
            self._load_all_configs()
            self._load_env_variables()
            logger.info("Configuration loaded successfully")
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
    
    def _load_all_configs(self) -> None:
        """Load all YAML config files"""
        config_files = [
            "blog_config.yaml",
            "llm_config.yaml",
            "schedule_config.yaml"
        ]
        
        for config_file in config_files:
            try:
                self._config_cache[config_file] = self._load_yaml(config_file)
            except FileNotFoundError:
                logger.warning(f"Config file {config_file} not found, skipping")
            except Exception as e:
                logger.error(f"Error loading {config_file}: {e}")
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load single YAML configuration file"""
        filepath = os.path.join(self.config_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logger.debug(f"Loaded config from {filename}")
                return config or {}
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {filename}: {e}")
            raise
    
    def _load_env_variables(self) -> None:
        """Load environment variables from .env file"""
        try:
            env_file = ".env"
            if os.path.exists(env_file):
                self._env_cache = dotenv_values(env_file)
                logger.debug(f"Loaded {len(self._env_cache)} environment variables")
            else:
                logger.warning(".env file not found, using system environment")
                self._env_cache = dict(os.environ)
        except Exception as e:
            logger.error(f"Error loading environment variables: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Config key (e.g., "blog.name", "llm.groq.model")
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        
        Example:
            >>> config.get("blog.name")
            "AI & Tech Insights"
            >>> config.get("missing.key", "default_value")
            "default_value"
        """
        try:
            keys = key.split('.')
            
            # Search through all loaded config files
            for config_data in self._config_cache.values():
                if isinstance(config_data, dict) and keys[0] in config_data:
                    value = config_data[keys[0]]
                    for k in keys[1:]:
                        if isinstance(value, dict):
                            value = value.get(k)
                        else:
                            return default
                    return value if value is not None else default
            
            # Try environment variables (keys are usually ENV_VAR_NAME)
            env_key = "_".join(keys).upper()
            return self._env_cache.get(env_key, default)
        
        except Exception as e:
            logger.warning(f"Error retrieving config key {key}: {e}")
            return default
    
    def get_blog_config(self) -> Dict[str, Any]:
        """Get full blog configuration"""
        return self._config_cache.get("blog_config.yaml", {})
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get full LLM configuration"""
        return self._config_cache.get("llm_config.yaml", {})
    
    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get environment variable safely.
        
        Args:
            key: Environment variable name (e.g., "GROQ_API_KEY")
            default: Default value if not set
        
        Returns:
            Environment variable value or default
        """
        value = self._env_cache.get(key)
        if value is None:
            logger.warning(f"Environment variable {key} not set, using default")
        return value or default
    
    def get_all_topics(self) -> List[Dict[str, Any]]:
        """Get all blog topics from configuration"""
        return self.get("blog.topics", [])
    
    def get_topic_weights(self) -> Dict[str, float]:
        """Get topic selection weights"""
        topics = self.get_all_topics()
        return {topic['name']: topic.get('weight', 1.0) for topic in topics}
    
    def get_llm_model(self) -> str:
        """Get primary LLM model name"""
        primary = self.get("llm.primary", "groq")
        return self.get(f"llm.{primary}.model", "mixtral-8x7b-32768")
    
    def get_publish_time(self) -> str:
        """Get scheduled publish time (HH:MM)"""
        return self.get("blog.scheduling.publish_time", "08:00")
    
    def get_timezone(self) -> str:
        """Get configured timezone"""
        return self.get("blog.scheduling.timezone", "Asia/Singapore")
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if feature is enabled in config"""
        return self.get(f"{feature}.enabled", False)
    
    def validate_config(self) -> bool:
        """Validate critical configuration values"""
        required_keys = [
            "blog.name",
            "blog.scheduling.publish_time",
        ]
        
        for key in required_keys:
            if not self.get(key):
                logger.error(f"Required config missing: {key}")
                return False
        
        # Check if LLM config exists
        llm_config = self.get_llm_config()
        if not llm_config:
            logger.error("LLM configuration file not found")
            return False
        
        logger.info("Configuration validation passed")
        return True

# Singleton instance
config = ConfigManager()
