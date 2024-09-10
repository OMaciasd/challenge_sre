import logging
from config.config import Config

logger = logging.getLogger(__name__)


def parse_rabbitmq_url():
    """
    Analiza la URL de RabbitMQ desde la configuración.
    """
    url = Config.RABBITMQ_URI
    if not url:
        logger.error("RABBITMQ_URI no está configurado.")
        raise ValueError("RABBITMQ_URI no está configurado.")

    return url
