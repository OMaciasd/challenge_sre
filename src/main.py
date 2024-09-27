import os
import platform
import socket
import logging
import psycopg2
from utils.secrets_utils import validate_secrets
from app import create_app


class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1']
    POSTGRES_DB = os.getenv('TF_VAR_postgres_db')
    POSTGRES_USER = os.getenv('TF_VAR_postgres_user')
    POSTGRES_PASSWORD = os.getenv('TF_VAR_postgres_password')
    HOST = os.getenv('TF_VAR_host', 'localhost')
    RABBITMQ_URI = os.getenv('TF_VAR_rabbitmq_uri')

    @staticmethod
    def validate():
        required_vars = [
            'TF_VAR_postgres_db',
            'TF_VAR_postgres_user',
            'TF_VAR_postgres_password',
            'TF_VAR_host',
            'TF_VAR_rabbitmq_uri'
        ]

        for var in required_vars:
            if not os.getenv(var):
                raise EnvironmentError(
                    f"{var} must be set in environment variables."
                )


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Logging is set up.")
    return logger


def connect_to_rabbitmq(rabbitmq_url, logger):
    import pika
    try:
        parameters = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(parameters)
        logger.info("Successfully connected to RabbitMQ")
        return connection
    except Exception as e:
        logger.error("Failed to connect to RabbitMQ: %s", e)
        return None


def get_host_ip(default='127.0.0.1', logger=None):
    current_os = platform.system()
    try:
        if current_os == "Linux":
            import netifaces
            interface = 'enp0s8'
            return netifaces.ifaddresses(
                interface
            )[netifaces.AF_INET][0]['addr']
        elif current_os == "Windows":
            return socket.gethostbyname(socket.gethostname())
        else:
            if logger:
                logger.warning("Unsupported operating system")
            return default
    except (ValueError, KeyError, IndexError, ImportError):
        if logger:
            logger.error("Error obtaining IP address. Using default value.")
        return default


def main():
    logger = setup_logging()

    config = Config()

    try:
        secrets = validate_secrets(config)
    except ValueError as e:
        logger.critical(e)
        return

    logger.info("Starting the application...")

    app = create_app()

    db_url = (
        f"postgres://{secrets['POSTGRES_USER']}:{secrets['POSTGRES_PASSWORD']}"
        f"@{secrets['HOST']}:{secrets['POSTGRES_PORT']}/"
        f"{secrets['POSTGRES_DB']}"
    )
    rabbitmq_uri = secrets['RABBITMQ_URI']

    logger.info("Connecting to database: %s", db_url)

    try:
        conn = psycopg2.connect(db_url)
        logger.info("Successfully connected to the database.")

        with conn.cursor() as cursor:
            cursor.execute("SELECT 1;")
            logger.info("Database query executed successfully.")

    except Exception as e:
        logger.error("Failed to connect to the database: %s", e)
        return

    rabbitmq_connection = connect_to_rabbitmq(rabbitmq_uri, logger)
    if rabbitmq_connection is None:
        logger.warning("RabbitMQ is not available, continuing without it.")

    app.run(host='127.0.0.1', port=5000)


if __name__ == "__main__":
    main()
