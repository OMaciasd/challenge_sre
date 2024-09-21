import os
from dotenv import load_dotenv

env_file = os.getenv('ENV_FILE', '.env')
load_dotenv(env_file)


class Config:
    """Base configuration."""
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1']
    DATABASE_URL = os.getenv('DATABASE_URL', 'localhost')
    RABBITMQ_URI = os.getenv('RABBITMQ_URI', 'localhost')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URL = os.getenv('DEVELOPMENT_DATABASE_URL', 'development-database-url')
    RABBITMQ_URI = os.getenv('DEVELOPMENT_RABBITMQ_URI', 'development-rabbitmq-uri')


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('TESTING_DATABASE_URL', 'test-database-url')
    RABBITMQ_URI = os.getenv('TESTING_RABBITMQ_URI', 'test-rabbitmq-uri')


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    DATABASE_URL = os.getenv('PRODUCTION_DATABASE_URL', 'prod-database-url')
    RABBITMQ_URI = os.getenv('PRODUCTION_RABBITMQ_URI', 'prod-rabbitmq-uri')


def get_config():
    env = os.getenv('ENVIRONMENT', 'development')
    if env == 'production':
        return ProductionConfig()
    elif env == 'test':
        return TestingConfig()
    elif env == 'development':
        return DevelopmentConfig()
    else:
        raise ValueError(f"Unknown environment: {env}")


config = get_config()
