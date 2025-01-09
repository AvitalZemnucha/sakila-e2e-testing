import pytest
import mysql.connector


@pytest.fixture
def db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="avitalz",
        database="sakila"
    )
    yield connection
    connection.close()


@pytest.fixture
def db_cursor(db_connection):
    """Provide a reusable database cursor for tests."""
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()
