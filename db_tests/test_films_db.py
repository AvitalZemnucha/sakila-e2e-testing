import pytest
import mysql.connector


def test_film_count(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM film')
    result = cursor.fetchone()
    print(result)
    assert result[0] > 0


def test_title(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT title FROM film')
    result = cursor.fetchall()
    print(result[1000])


def test_one_title(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT title FROM film WHERE film_id = 1000')
    result = cursor.fetchone()
    assert "ZORRO ARK" in result[0]
