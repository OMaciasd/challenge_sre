import pytest
from unittest.mock import patch, MagicMock
from config.config import Config
from utils.rabbitmq_utils import parse_rabbitmq_url
from utils.secrets_utils import validate_secrets

@pytest.fixture
def set_rabbitmq_config():
    return Config.RABBITMQ_URI

@pytest.mark.timeout(5)
def test_validate_secrets_all_vars_set(set_rabbitmq_config):
    try:
        validate_secrets()
    except ValueError:
        pytest.fail("validate_secrets raised ValueError unexpectedly!")

@patch('pika.BlockingConnection')
@pytest.mark.timeout(10)
def test_parse_rabbitmq_url(mock_blocking_connection, set_rabbitmq_config):
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_blocking_connection.return_value = mock_connection

    result = parse_rabbitmq_url()
    expected_url = set_rabbitmq_config

    if result != expected_url:
        pytest.fail(f"Expected '{expected_url}', but got '{result}'")

    mock_blocking_connection.assert_called_once()
