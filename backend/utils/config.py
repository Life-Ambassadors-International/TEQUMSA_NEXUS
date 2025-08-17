"""Configuration utilities for TEQUMSA Level 100."""
import os
from typing import Optional, Dict, Any
from pathlib import Path


class Config:
    """Configuration management class."""
    
    def __init__(self):
        """Initialize configuration."""
        self.env = os.environ.get('ENVIRONMENT', 'development')
        self.debug = os.environ.get('DEBUG', 'false').lower() == 'true'
        
        # Database configuration
        self.database_url = os.environ.get('DATABASE_URL', 'sqlite:///tequmsa.db')
        
        # Redis configuration
        self.redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
        
        # API configuration
        self.api_host = os.environ.get('API_HOST', '0.0.0.0')
        self.api_port = int(os.environ.get('API_PORT', '8000'))
        
        # Authentication
        self.jwt_secret = os.environ.get('JWT_SECRET', 'dev-secret-key')
        self.jwt_algorithm = os.environ.get('JWT_ALGORITHM', 'HS256')
        
        # External APIs
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        self.elevenlabs_api_key = os.environ.get('ELEVENLABS_API_KEY')
        
        # TEQUMSA specific
        self.default_biome = os.environ.get('DEFAULT_BIOME', 'peaceful_meadow')
        self.max_entities_per_region = int(os.environ.get('MAX_ENTITIES_PER_REGION', '1000'))
        
        # Subscription system
        self.subscription_config_dir = os.environ.get(
            'SUBSCRIPTION_CONFIG_DIR',
            str(Path(__file__).parent.parent / 'subscription')
        )
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return getattr(self, key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }


# Global configuration instance
_config = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config():
    """Reload configuration from environment."""
    global _config
    _config = Config()