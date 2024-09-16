import pytest
import os
from unittest.mock import patch, MagicMock
from config.config import Config
from utils.rabbitmq_utils import parse_rabbitmq_url
from utils.secrets_utils import validate_secrets

def get_test_rabbitmq_url():
    return Config.RABBITMQ_URI

@pytest.fixture
def set_rabbitmq_env_var():
    test_url = get_test_rabbitmq_url()
    os.environ['RABBITMQ_URI'] = test_url
    yield test_url
    del os.environ['RABBITMQ_URI']

def test_validate_secrets_all_vars_set(set_rabbitmq_env_var):
    try:
        validate_secrets()
    except ValueError:
        pytest.fail("validate_secrets raised ValueError unexpectedly!")

@patch('utils.rabbitmq_utils.pika.BlockingConnection')
def test_parse_rabbitmq_url(mock_blocking_connection, set_rabbitmq_env_var):
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_blocking_connection.return_value = mock_connection

    result = parse_rabbitmq_url()
    expected_url = set_rabbitmq_env_var

    if result != expected_url:
        pytest.fail(f"Expected '{expected_url}', but got '{result}'")
