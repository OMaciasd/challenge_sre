from config.config import Config
import pika

def parse_rabbitmq_url():
    uri = Config.RABBITMQ_URI
    if not uri:
        raise ValueError("RABBITMQ_URI is not set")
    
    connection_parameters = pika.URLParameters(uri)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
        
    return uri
