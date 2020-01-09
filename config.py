"""Configure application"""
import os


class Config:
    """Default application configuration"""
    DEBUG = True  # Turns on debugging features in Flask
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')


class ProductionConfig(Config):
    """Production application configuration"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development application configuration"""
    DEBUG = True


class TestingConfig(Config):
    """Testing application configuration"""
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
