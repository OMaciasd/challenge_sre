import pytest
from unittest.mock import patch
from config.config import Config
from utils.database_utils import parse_database_url
from utils.secrets_utils import validate_secrets


@patch.object(Config, 'DATABASE_URL', 'sqlite:///:memory:')
def test_validate_secrets_all_vars_set():
    try:
        validate_secrets()
    except ValueError:
        pytest.fail("validate_secrets raised ValueError unexpectedly!")


@patch.object(Config, 'DATABASE_URL', None)
def test_validate_secrets_missing_database_url():
    with pytest.raises(ValueError) as excinfo:
        validate_secrets()
    if "Required environment variables are missing: DATABASE_URL" not in str(
        excinfo.value
    ):
        pytest.fail(
            "Expected error message to contain 'DATABASE_URL',"
            f"but got {excinfo.value}"
        )


@patch.object(Config, 'DATABASE_URL', 'sqlite:///:memory:')
def test_parse_database_url():
    result = parse_database_url()

    expected_result = {
        'dbname': ':memory:',
        'user': None,
        'password': None,
        'host': None,
        'port': None
    }

    if result != expected_result:
        pytest.fail(
            f"Expected {expected_result}, but got {result}"
        )
