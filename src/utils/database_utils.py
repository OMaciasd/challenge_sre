import logging
from urllib.parse import urlparse, ParseResult
from config.config import Config

logger = logging.getLogger(__name__)


def parse_database_url():
    """
    Parses the database URL from configuration, returns a dictionary.
    """
    url = Config.DATABASE_URL
    if not url:
        logger.error("DATABASE_URL is not configured.")
        raise ValueError("DATABASE_URL is not configured.")

    try:
        parsed_url: ParseResult = urlparse(url)
    except Exception as e:
        logger.error(f"Error parsing DATABASE_URL: {e}")
        raise

    return {
        'dbname': parsed_url.path[1:],
        'user': parsed_url.username,
        'password': parsed_url.password,
        'host': parsed_url.hostname,
        'port': parsed_url.port
    }
