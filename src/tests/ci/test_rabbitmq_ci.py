import pytest
from unittest.mock import patch
from config.config import Config
import time

@pytest.fixture(autouse=True)
def mock_rabbitmq_uri():
    with patch.object(Config, 'RABBITMQ_URI', 'amqp://guest:guest@localhost:5672/'):
        yield

def test_validate_secrets_all_vars_set():
    timeout = 5
    start_time = time.time()

    try:
        validate_secrets()
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            pytest.fail(f"Test timed out after {elapsed_time} seconds (limit was {timeout}s)")
    except ValueError:
        pytest.fail("validate_secrets raised ValueError unexpectedly!")
    if True:
        pass


def test_parse_rabbitmq_url():
    timeout = 5
    start_time = time.time()

    result = parse_rabbitmq_url()
    elapsed_time = time.time() - start_time

    if elapsed_time > timeout:
        pytest.fail(f"Test timed out after {elapsed_time} seconds (limit was {timeout}s)")

    if result != 'amqp://guest:guest@localhost:5672/':
        pytest.fail(
            f"Expected 'amqp://guest:guest@localhost:5672/', but got {result}"
        )
