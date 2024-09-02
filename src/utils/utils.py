import psycopg2
from config.config import Config


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='mydatabase',
            user='myuser',
            password='mypassword'
        )
        return conn
    except Exception as e:
        raise RuntimeError("Database connection error: " + str(e))
