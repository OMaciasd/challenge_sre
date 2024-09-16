import pytest
import os
from config.config import Config
from utils.rabbitmq_utils import parse_rabbitmq_url
from utils.secrets_utils import validate_secrets

@pytest.fixture
def set_rabbitmq_env_var():
    os.environ['RABBITMQ_URI'] = Config.RABBITMQ_URI
    yield os.environ['RABBITMQ_URI']
    del os.environ['RABBITMQ_URI']

def test_validate_secrets_all_vars_set(set_rabbitmq_env_var):
    try:
        validate_secrets()
    except ValueError:
        pytest.fail("validate_secrets raised ValueError unexpectedly!")

def test_parse_rabbitmq_url(set_rabbitmq_env_var):
    result = parse_rabbitmq_url()
    expected_url = set_rabbitmq_env_var
    if result != expected_url:
        pytest.fail(f"Expected '{expected_url}', but got '{result}'")
