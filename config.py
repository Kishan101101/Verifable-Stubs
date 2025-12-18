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
    SQLALCHEMY_ECHO: bool = True
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

# Create config mapping
config = {
    'development': DevelopmentConfig(),
    'production': ProductionConfig(),
    'testing': TestingConfig(),
}

def get_config(config_name: str = 'development') -> Settings:
    """Get configuration object"""
    return config.get(config_name, config['development'])


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
