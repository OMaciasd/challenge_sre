import os
import pytest
import psycopg2
from utils.database_utils import parse_database_url
from utils.secrets_utils import validate_secrets


def test_database_connection():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        pytest.fail("DATABASE_URL environment variable is not set.")

    print(f"Database URL: {database_url}")

    try:
        db_info = parse_database_url()
    except Exception as e:
        pytest.fail(f"Failed to parse DATABASE_URL: {e}")

    print(f"Parsed DB Info: {db_info}")

    try:
        conn = psycopg2.connect(
            dbname=db_info['dbname'],
            user=db_info['user'],
            password=db_info['password'],
            host=db_info['host'],
            port=db_info['port']
        )
        if conn is None:
            pytest.fail("Failed to establish a connection to the database.")
    except psycopg2.OperationalError as e:
        pytest.fail(f"Operational error connecting to the database: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error connecting to the database: {e}")
    finally:
        if conn:
            conn.close()
