import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Base configuration for FastAPI"""
    APP_ENV: str = "development"
    DEBUG: bool = False
    API_TITLE: str = os.getenv('API_TITLE', 'Verifiable Stubs APIs')
    API_VERSION: str = os.getenv('API_VERSION', '1.0.0')
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@127.0.0.1:5433/verifiable_stubs')
    # Disable SQLAlchemy echo by default to avoid verbose SQL logs
    SQLALCHEMY_ECHO: bool = False
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Settings):
    """Development configuration"""
    DEBUG: bool = True
    APP_ENV: str = "development"
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@127.0.0.1:5433/verifiable_stubs')

class ProductionConfig(Settings):
    """Production configuration"""
    DEBUG: bool = False
    APP_ENV: str = "production"
    DATABASE_URL: str = os.getenv('DATABASE_URL')

class TestingConfig(Settings):
    """Testing configuration"""
    DEBUG: bool = True
    APP_ENV: str = "testing"
    DATABASE_URL: str = 'sqlite:///./test.db'

# Create config mapping (map names to classes)
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}


def get_config(config_name: str = 'development') -> Settings:
    """Get configuration instance for the given name.

    Returns an instantiated `Settings` subclass so callers can access
    attributes as `settings.API_TITLE`.
    """
    cfg_class = config.get(config_name, config['default'])
    return cfg_class()
