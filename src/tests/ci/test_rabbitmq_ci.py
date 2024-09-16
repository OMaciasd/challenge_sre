import pytest
import os
from unittest.mock import patch, Mock
from config.config import Config
from utils.rabbitmq_utils import parse_rabbitmq_url
from utils.secrets_utils import validate_secrets

@pytest.fixture(autouse=True)
def mock_rabbitmq_uri():
    with patch.dict(os.environ, {'RABBITMQ_URI': 'mocked_rabbitmq_url'}):
        yield

@pytest.mark.timeout(5)
def test_validate_secrets_all_vars_set():
    try:
        validate_secrets()
    except ValueError:
        pytest.fail("validate_secrets raised ValueError unexpectedly!")

@pytest.mark.timeout(5)
@patch('utils.rabbitmq_utils.pika.BlockingConnection')
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
