import pika
import logging
from config.config import Config

logger = logging.getLogger(__name__)

def parse_rabbitmq_url():
    """
    Analyzes RabbitMQ URL from the configuration.
    """
    url = Config.RABBITMQ_URI
    if not url:
        logger.error("RABBITMQ_URI is not configured.")
        raise ValueError("RABBITMQ_URI is not configured.")

    try:
        connection_params = pika.ConnectionParameters(
            host=url,
            socket_timeout=10 
        )
        connection = pika.BlockingConnection(connection_params)
        connection.close()
    except Exception as e:
        logger.error(f"Error connecting to RabbitMQ: {e}")
        raise

    return url
