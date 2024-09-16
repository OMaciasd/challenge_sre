import pika
import requests
import os

def test_log_integration():
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'localhost')
    elasticsearch_url = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(rabbitmq_url)
    )
    channel = connection.channel()
    channel.queue_declare(queue='log_queue')
    channel.basic_publish(exchange='',
                          routing_key='log_queue',
                          body='test log message')
    connection.close()

    try:
        response = requests.get(
            f'{elasticsearch_url}/logs-*/_search?q=test+log+message',
            timeout=10
        )
        if response.status_code == 200:
            if 'test log message' in response.text:
                print("Test passed: Log message found in Elasticsearch.")
            else:
                print("Test failed: Log message not found in Elasticsearch.")
        else:
            print(
                f"Test failed: Elasticsearch returned status code {response.status_code}."
            )
    except requests.exceptions.RequestException as e:
        print(f"Test failed: An error occurred - {e}")
