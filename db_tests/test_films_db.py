import pytest
import mysql.connector


def test_film_count(db_cursor):
    db_cursor.execute('SELECT COUNT(*) FROM film')
    result = db_cursor.fetchone()
    print(result)
    assert result[0] > 0


def test_title(db_cursor):
    db_cursor.execute('SELECT title FROM film')
    result = db_cursor.fetchall()
    print(result[1000])


def test_one_title(db_cursor):
    db_cursor.execute('SELECT title FROM film WHERE film_id = 1000')
    result = db_cursor.fetchone()
    assert "ZORRO ARK" in result[0]
