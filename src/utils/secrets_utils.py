import logging
from config.config import Config

logger = logging.getLogger(__name__)


def validate_secrets():
    """
    Validates that all required environment variables are configured.
    """
    required_env_vars = ['DATABASE_URL', 'RABBITMQ_URI']
    missing_vars = [
        var for var in required_env_vars if not getattr(Config, var, None)
    ]

    if missing_vars:
        missing_vars_str = ', '.join(missing_vars)
        message = (
            "The following environment variables are missing: "
            f"{missing_vars_str}"
        )

        logger.error(message)
        raise ValueError(
            f"Required environment variables are missing: {missing_vars_str}"
        )
