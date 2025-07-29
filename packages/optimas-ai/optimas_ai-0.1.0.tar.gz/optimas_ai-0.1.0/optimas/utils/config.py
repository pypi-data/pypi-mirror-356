from typing import Dict, Any, Optional
from contextlib import contextmanager
import os
import yaml
import os.path as osp
from omegaconf import OmegaConf

class ConfigManager:
    """
    Manages LLM configurations for individual modules.
    Uses a single config file with explicit module settings.
    """
    def __init__(self, module_configs: Dict[str, Dict[str, Any]]):
        """
        Initialize the ConfigManager with module-specific configurations.
        
        Args:
            module_configs (Dict[str, Dict[str, Any]]): Module-specific configurations.
        """
        # Store module-specific configs
        self.module_configs = module_configs or {}
        
        # Validate required fields in each module config
        for module_name, config in self.module_configs.items():
            required_fields = ["model", "temperature", "max_tokens"]
            missing = [field for field in required_fields if field not in config]
            if missing:
                raise ValueError(f"Module '{module_name}' is missing required config fields: {missing}")
    
    @contextmanager
    def override(self, module_name, **config_overrides):
        """
        Context manager for temporarily overriding configurations.
        
        Args:
            module_name (str): Module to override settings for.
            **config_overrides: Configuration overrides.
        """
        if module_name not in self.module_configs:
            raise ValueError(f"Module '{module_name}' not found in configuration")
            
        old_config = self.module_configs[module_name].copy()
        self.module_configs[module_name].update(config_overrides)
        
        try:
            yield
        finally:
            self.module_configs[module_name] = old_config
    
    def get_config(self, module_name, **runtime_overrides):
        """
        Get effective configuration for a module.
        
        Args:
            module_name (str): Module name to get config for.
            **runtime_overrides: Override specific parameters at runtime.
            
        Returns:
            Dict[str, Any]: Effective configuration.
        """
        if module_name not in self.module_configs:
            raise ValueError(f"Module '{module_name}' not found in configuration")
            
        # Start with module's config
        effective_config = self.module_configs[module_name].copy()
        
        # Apply runtime overrides (highest priority)
        if runtime_overrides:
            effective_config.update(runtime_overrides)
            
        return effective_config
        
    def get_module_names(self):
        """
        Get all configured module names.
        
        Returns:
            List[str]: List of module names in the configuration.
        """
        return list(self.module_configs.keys())
    
    def update_module_config(self, module_name, **config_updates):
        """
        Permanently update a module's configuration.
        
        Args:
            module_name (str): Module name to update
            **config_updates: Configuration updates to apply
        """
        if module_name not in self.module_configs:
            raise ValueError(f"Module '{module_name}' not found in configuration")
            
        self.module_configs[module_name].update(config_updates)
        
    def update_sampling_config(self, **config_updates):
        """
        Update the sampling configuration.
        
        Args:
            **config_updates: Configuration updates to apply
        """
        self.sampling_config.update(config_updates)
    
    @staticmethod
    def from_yaml(config_path):
        """
        Create a ConfigManager from a single YAML configuration file.
        
        Args:
            config_path (str): Path to configuration file.
            
        Returns:
            ConfigManager: Configured instance.
        """
        if not osp.exists(config_path):
            raise FileNotFoundError(f"Config file {config_path} not found")
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        module_configs = {}
        sampling_config = {}
        
        for key, value in config.items():
            if key == 'sampling':
                sampling_config = value
            else:
                module_configs[key] = value
        
        manager = ConfigManager(module_configs=module_configs)
        
        if sampling_config:
            manager.sampling_config = sampling_config
        else:
            manager.sampling_config = {
                "temperature": 1.2,
                "size": 5
            }
            
        return manager