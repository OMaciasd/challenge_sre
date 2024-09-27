import os
import pytest
import psycopg2
from utils.database_utils import parse_database_url


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

    conn = None

    try:
        conn = psycopg2.connect(
            dbname=db_info['dbname'],
            user=db_info['user'],
            password=db_info['password'],
            host=db_info['host'],
            port=db_info['port']
        )
        if conn is None:
            pytest.fail("Database connection should not be None.")
        else:
            print("Database connection established successfully.")
    except psycopg2.Error as e:
        pytest.fail(f"Database connection failed: {e}")
    finally:
        if conn:
            conn.close()
