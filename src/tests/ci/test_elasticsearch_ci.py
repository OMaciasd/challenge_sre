import os
import pika
import requests
from unittest.mock import patch, MagicMock
import pytest
from config.config import Config
from utils.rabbitmq_utils import parse_rabbitmq_url
from utils.secrets_utils import validate_secrets

@pytest.fixture(autouse=True)
def mock_environment():
    with patch.dict(os.environ, {
        'RABBITMQ_URL': 'mocked_rabbitmq_url',
        'ELASTICSEARCH_URL': 'http://mocked_elasticsearch_url'
    }):
        yield

def test_log_integration():
    with patch('pika.BlockingConnection') as MockConnection:
        mock_channel = MagicMock()
        mock_channel.queue_declare.return_value = None
        mock_channel.basic_publish.return_value = None
        MockConnection.return_value.channel.return_value = mock_channel
        
        connection = MockConnection(
            pika.ConnectionParameters(
                'mocked_rabbitmq_url'
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='log_queue')
        channel.basic_publish(exchange='',
                              routing_key='log_queue',
                              body='test log message')

    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"hits": {"hits": [{"_source": {"message": "test log message"}}]}}'
        mock_get.return_value = mock_response
        
        response = requests.get(
            'http://mocked_elasticsearch_url/logs-*/_search?q=test+log+message',
            timeout=10
        )
        
        if response.status_code == 200:
            if 'test log message' in response.text:
                print("Test passed: Log message found in Elasticsearch.")
            else:
                print("Test failed: Log message not found in Elasticsearch.")
        else:
            print(f"Test failed: Elasticsearch returned status code {response.status_code}.")
            
@pytest.mark.timeout(5)
def test_validate_secrets_all_vars_set():
    try:
        validate_secrets()
    except ValueError:
        pytest.fail("validate_secrets raised ValueError unexpectedly!")

@pytest.mark.timeout(5)
@patch('pika.BlockingConnection')
def test_parse_rabbitmq_url(mock_blocking_connection):
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_blocking_connection.return_value = mock_connection

    result = parse_rabbitmq_url()

    mock_blocking_connection.assert_called_once()
    
    expected_url = os.getenv('RABBITMQ_URL', 'mocked_rabbitmq_url')
    if result != expected_url:
        pytest.fail(f"Expected '{expected_url}', but got {result}")
