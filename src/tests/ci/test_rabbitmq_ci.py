import pytest
from unittest.mock import patch
from config.config import Config
from utils.rabbitmq_utils import parse_rabbitmq_url
from utils.secrets_utils import validate_secrets

@pytest.fixture(autouse=True)
def mock_rabbitmq_uri():
    with patch.object(Config, 'RABBITMQ_URI', 'amqp://guest:guest@localhost:5672/'):
        yield

@pytest.mark.timeout(5)
def test_validate_secrets_all_vars_set():
    try:
        validate_secrets()
    except ValueError:
        pytest.fail("validate_secrets raised ValueError unexpectedly!")

@pytest.mark.timeout(5)
def test_parse_rabbitmq_url():
    result = parse_rabbitmq_url()
    
    if result != 'amqp://guest:guest@localhost:5672/':
        pytest.fail(f"Expected 'amqp://guest:guest@localhost:5672/', but got {result}")
