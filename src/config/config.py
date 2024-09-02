import os

class Config:
    """Base configuration."""
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    RABBITMQ_URI = os.getenv('RABBITMQ_URI', 'default-rabbitmq-uri')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/mydatabase')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    RABBITMQ_URI = os.getenv('DEVELOPMENT_RABBITMQ_URI', 'dev-rabbitmq-uri')
    DATABASE_URL = os.getenv('DEVELOPMENT_DATABASE_URL', 'dev-database-url')

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    RABBITMQ_URI = os.getenv('TESTING_RABBITMQ_URI', 'test-rabbitmq-uri')
    DATABASE_URL = os.getenv('TESTING_DATABASE_URL', 'test-database-url')

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    RABBITMQ_URI = os.getenv('PRODUCTION_RABBITMQ_URI', 'prod-rabbitmq-uri')
    DATABASE_URL = os.getenv('PRODUCTION_DATABASE_URL', 'prod-database-url')

class LocalConfig(Config):
    """Local configuration."""
    DEBUG = True
    RABBITMQ_URI = os.getenv('LOCAL_RABBITMQ_URI', 'local-rabbitmq-uri')
    DATABASE_URL = os.getenv('LOCAL_DATABASE_URL', 'sqlite:///local.db')

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'local': LocalConfig,
}
