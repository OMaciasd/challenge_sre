class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your-secret-key'
    RABBITMQ_URI = 'your-default-rabbitmq-uri'
    DATABASE_URL = 'your-default-database-url'


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    RABBITMQ_URI = 'dev-rabbitmq-uri'
    DATABASE_URL = 'dev-database-url'


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    RABBITMQ_URI = 'test-rabbitmq-uri'
    DATABASE_URL = 'test-database-url'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    RABBITMQ_URI = 'prod-rabbitmq-uri'
    DATABASE_URL = 'prod-database-url'


class LocalConfig(Config):
    """Local configuration."""
    DEBUG = True
    RABBITMQ_URI = 'local-rabbitmq-uri'
    DATABASE_URL = 'sqlite:///local.db'


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'local': LocalConfig,
}
