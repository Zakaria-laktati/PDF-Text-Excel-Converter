"""
Configuration management for PDF Converter.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import json
from dataclasses import dataclass, asdict
from src.utils.exceptions import ConfigurationError

@dataclass
class OCRConfig:
    """OCR configuration settings."""
    tesseract_path: str = ""
    default_language: str = "eng"
    supported_languages: list = None
    confidence_threshold: int = 50
    
    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = ["eng", "fra"]

@dataclass
class ProcessingConfig:
    """Processing configuration settings."""
    max_file_size_mb: int = 100
    temp_dir: str = "/tmp"
    output_dir: str = "./output"
    enable_caching: bool = True
    max_workers: int = 4

@dataclass
class UIConfig:
    """User interface configuration."""
    page_title: str = "PDF Converter Pro"
    max_upload_size_mb: int = 100
    show_preview: bool = True
    theme: str = "light"

@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "standard"  # standard, json
    file_path: Optional[str] = None
    console_output: bool = True

@dataclass
class AppConfig:
    """Main application configuration."""
    ocr: OCRConfig
    processing: ProcessingConfig
    ui: UIConfig
    logging: LoggingConfig
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'AppConfig':
        """Create configuration from dictionary."""
        return cls(
            ocr=OCRConfig(**config_dict.get('ocr', {})),
            processing=ProcessingConfig(**config_dict.get('processing', {})),
            ui=UIConfig(**config_dict.get('ui', {})),
            logging=LoggingConfig(**config_dict.get('logging', {}))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)

class ConfigManager:
    """Configuration manager for loading and managing application settings."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self._config: Optional[AppConfig] = None
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        return os.path.join(os.path.dirname(__file__), "..", "..", "config", "config.yaml")
    
    def load_config(self) -> AppConfig:
        """Load configuration from file and environment variables."""
        try:
            # Load from file
            config_dict = self._load_from_file()
            
            # Override with environment variables
            config_dict = self._override_with_env(config_dict)
            
            # Create configuration object
            self._config = AppConfig.from_dict(config_dict)
            
            return self._config
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {str(e)}")
    
    def _load_from_file(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not os.path.exists(self.config_path):
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    return yaml.safe_load(f) or {}
                elif self.config_path.endswith('.json'):
                    return json.load(f)
                else:
                    raise ConfigurationError(f"Unsupported config file format: {self.config_path}")
        except Exception as e:
            raise ConfigurationError(f"Failed to read config file: {str(e)}")
    
    def _override_with_env(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Override configuration with environment variables."""
        env_mappings = {
            'TESSERACT_PATH': ('ocr', 'tesseract_path'),
            'DEFAULT_LANGUAGE': ('ocr', 'default_language'),
            'MAX_FILE_SIZE_MB': ('processing', 'max_file_size_mb'),
            'TEMP_DIR': ('processing', 'temp_dir'),
            'OUTPUT_DIR': ('processing', 'output_dir'),
            'LOG_LEVEL': ('logging', 'level'),
            'LOG_FILE_PATH': ('logging', 'file_path'),
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                if section not in config_dict:
                    config_dict[section] = {}
                
                # Type conversion
                if key in ['max_file_size_mb', 'max_workers', 'confidence_threshold']:
                    config_dict[section][key] = int(value)
                elif key in ['enable_caching', 'show_preview', 'console_output']:
                    config_dict[section][key] = value.lower() in ('true', '1', 'yes')
                else:
                    config_dict[section][key] = value
        
        return config_dict
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'ocr': {
                'tesseract_path': '',
                'default_language': 'eng',
                'supported_languages': ['eng', 'fra'],
                'confidence_threshold': 50
            },
            'processing': {
                'max_file_size_mb': 100,
                'temp_dir': '/tmp',
                'output_dir': './output',
                'enable_caching': True,
                'max_workers': 4
            },
            'ui': {
                'page_title': 'PDF Converter Pro',
                'max_upload_size_mb': 100,
                'show_preview': True,
                'theme': 'light'
            },
            'logging': {
                'level': 'INFO',
                'format': 'standard',
                'file_path': None,
                'console_output': True
            }
        }
    
    def save_config(self, config: AppConfig) -> None:
        """Save configuration to file."""
        try:
            config_dir = os.path.dirname(self.config_path)
            os.makedirs(config_dir, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    yaml.dump(config.to_dict(), f, default_flow_style=False)
                elif self.config_path.endswith('.json'):
                    json.dump(config.to_dict(), f, indent=2)
            
            self._config = config
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {str(e)}")
    
    @property
    def config(self) -> AppConfig:
        """Get current configuration."""
        if self._config is None:
            self._config = self.load_config()
        return self._config

# Global configuration manager instance
config_manager = ConfigManager()