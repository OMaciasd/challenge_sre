import pytest
import os
from unittest.mock import patch, MagicMock
from utils.rabbitmq_utils import parse_rabbitmq_url

@pytest.fixture(autouse=True)
def mock_rabbitmq_uri():
    rabbitmq_uri = 'mocked_rabbitmq_uri'
    with patch.dict(os.environ, {'RABBITMQ_URI': rabbitmq_uri}):
        yield rabbitmq_uri

@pytest.mark.timeout(5)
@patch('utils.rabbitmq_utils.pika.BlockingConnection')
@patch('utils.rabbitmq_utils.pika.ConnectionParameters')
def test_parse_rabbitmq_url(mock_connection_parameters, mock_blocking_connection, mock_rabbitmq_uri):
    mock_connection = MagicMock()
    mock_blocking_connection.return_value = mock_connection
    mock_connection_parameters.return_value = MagicMock()

    result = parse_rabbitmq_url()

    if not mock_blocking_connection.called:
        pytest.fail("Expected BlockingConnection to be called once, but it was not.")

    if not mock_connection_parameters.called:
        pytest.fail("Expected ConnectionParameters to be called, but it was not.")

    call_args = mock_connection_parameters.call_args
    if not call_args:
        pytest.fail("ConnectionParameters was not called with any arguments.")
    
    connection_params = call_args[0][0]
    if connection_params.host != mock_rabbitmq_uri or connection_params.socket_timeout != 10:
        pytest.fail(f"Expected ConnectionParameters to be called with host='{mock_rabbitmq_uri}' and socket_timeout=10, but got host='{connection_params.host}' and socket_timeout={connection_params.socket_timeout}.")

    if result != mock_rabbitmq_uri:
        pytest.fail(f"Expected '{mock_rabbitmq_uri}', but got {result}.")
