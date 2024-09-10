from utils.rabbitmq_utils import parse_rabbitmq_url


def parse_rabbitmq_url(url):
    if not url.startswith('amqp://'):
        raise ValueError("Invalid RabbitMQ URI")
    try:
        credentials, address = url[7:].split('@')
        user = credentials
        host, port = address.split(':')
        port = port.rstrip('/')

        return {
            'host': host,
            'port': int(port),
            'user': user
        }
    except Exception as e:
        raise ValueError(f"Error parsing RabbitMQ URI: {e}")
