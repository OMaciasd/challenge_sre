import os
import logging

logger = logging.getLogger(__name__)


class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1']
    POSTGRES_DB = os.getenv('TF_VAR_postgres_db')
    POSTGRES_USER = os.getenv('TF_VAR_postgres_user')
    POSTGRES_PASSWORD = os.getenv('TF_VAR_postgres_password')
    HOST = os.getenv('TF_VAR_host', 'localhost')
    POSTGRES_URL = os.getenv('TF_VAR_postgres_url')
    RABBITMQ_URI = os.getenv('TF_VAR_rabbitmq_uri')
    POSTGRES_PORT = os.getenv('TF_VAR_postgres_port')

    @classmethod
    def validate(cls):
        required_vars = {
            'TF_VAR_postgres_db': cls.POSTGRES_DB,
            'TF_VAR_postgres_user': cls.POSTGRES_USER,
            'TF_VAR_postgres_password': cls.POSTGRES_PASSWORD,
            'TF_VAR_host': cls.HOST,
            'TF_VAR_postgres_url': cls.POSTGRES_URL,
            'TF_VAR_rabbitmq_uri': cls.RABBITMQ_URI,
            'TF_VAR_postgres_port': cls.POSTGRES_PORT
        }

        missing_vars = [
            var for var,
            value in required_vars.items(
            )
            if not value
        ]

        if missing_vars:
            missing_vars_str = ', '.join(missing_vars)
            logger.error("Missing environment variables: %s", missing_vars_str)
            raise EnvironmentError(
                "Required environment variables are missing:"
                f"{missing_vars_str}"
            )

        logger.info("All required environment variables are present.")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


def get_config():
    """Retrieve the appropriate configuration based on the environment."""
    env = os.getenv('ENVIRONMENT', 'development')

    config_map = {
        'production': ProductionConfig,
        'test': TestingConfig,
        'development': DevelopmentConfig
    }

    config_class = config_map.get(env)
    if not config_class:
        raise ValueError(f"Unknown environment: {env}")

    config_class.validate()
    return config_class()


config = get_config()
