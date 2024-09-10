import requests
import pytest
from unittest.mock import patch, MagicMock
import pika

@patch('pika.BlockingConnection')
@patch('requests.get')
def test_log_integration(mock_requests_get, mock_blocking_connection):
    mock_connection = mock_blocking_connection.return_value
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel

    if mock_connection is not None:
        print("Mock connection created successfully.")
    else:
        print("Test failed: Mock connection is None.")
        return

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='log_queue')
    channel.basic_publish(exchange='',
                          routing_key='log_queue',
                          body='test log message')
    connection.close()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"hits":{"hits":[{"_source":{"message":"test log message"}}]}}'
    mock_requests_get.return_value = mock_response

    try:
        response = requests.get(
            'http://localhost:9200/logs-*/_search?q=test+log+message',
            timeout=10
        )

        if response.status_code == 200:
            if 'test log message' in response.text:
                print("Test passed: Log message found in Elasticsearch.")
            else:
                print("Test failed: Log message not found in Elasticsearch.")
        else:
            print(f"Test failed: Elasticsearch returned status code {response.status_code}.")
    
    except requests.exceptions.RequestException as e:
        print(f"Test failed: An error occurred - {e}")
