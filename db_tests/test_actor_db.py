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


def test_actor_count(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM actor")
    result = cursor.fetchone()
    assert result[0] > 0


def test_actor_names(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT last_name, first_name FROM actor LIMIT 5")
    result = cursor.fetchall()
    assert len(result) == 5
    for first_name, last_name in result:
        assert len(first_name) > 0 and len(last_name) > 0
