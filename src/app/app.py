from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import pika
import os
from config import config_by_name

app = Flask(__name__)

def load_config():
    env = os.getenv('FLASK_ENV', 'development')
    print(f"Loading configuration for environment: {env}")
    app_config_class = config_by_name.get(env, config_by_name['development'])
    if not isinstance(app_config_class, type):
        raise TypeError(f"{app_config_class} is not a class")
    app_config = app_config_class()  # Crear una instancia de la configuración
    print(f"SECRET_KEY: {app_config.SECRET_KEY}")
    print(f"RABBITMQ_URI: {app_config.RABBITMQ_URI}")
    print(f"DATABASE_URL: {app_config.DATABASE_URL}")
    return app_config

app_config = load_config()
app.config.from_object(app_config)  # Asigna la configuración a la aplicación Flask

def initialize_rabbitmq():
    try:
        connection = pika.BlockingConnection(
            pika.URLParameters(app_config.RABBITMQ_URI)
        )
        channel = connection.channel()
        channel.queue_declare(queue='data_queue')
        return connection, channel
    except Exception as e:
        print(f"Error connecting to RabbitMQ: {e}")
        return None, None

def initialize_database():
    try:
        engine = create_engine(app_config.DATABASE_URL)
        with engine.connect():
            pass
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

connection, channel = initialize_rabbitmq()
engine = initialize_database()

if connection is None or engine is None:
    print("Switching to local configuration due to initialization failure.")
    app_config = config_by_name['local']()  # Asegúrate de crear una instancia
    app.config.from_object(app_config)  # Vuelve a asignar la configuración local si falla
    connection, channel = initialize_rabbitmq()
    engine = initialize_database()

@app.route('/')
def homepage():
    return "Hello, World!"

@app.route('/log', methods=['POST'])
def log_data():
    """Publica un mensaje en RabbitMQ."""
    log_message = request.json.get('message', '')
    if channel:
        channel.basic_publish(exchange='',
                              routing_key='data_queue',
                              body=log_message)
        return jsonify({
            'status': 'success',
            'message': 'Log sent to RabbitMQ'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'RabbitMQ connection not available'
        })

if __name__ == '__main__':
    app.run()
