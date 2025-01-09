import pytest
import mysql.connector


def test_actor_count(db_cursor):
    db_cursor.execute("SELECT COUNT(*) FROM actor")
    result = db_cursor.fetchone()
    assert result[0] > 0


def test_actor_names(db_cursor):
    db_cursor.execute("SELECT last_name, first_name FROM actor LIMIT 5")
    result = db_cursor.fetchall()
    assert len(result) == 5
    for first_name, last_name in result:
        assert len(first_name) > 0 and len(last_name) > 0


def test_actor_insertion(db_cursor):
    db_cursor.execute("INSERT INTO actor (first_name, last_name) VALUES (%s, %s)", ("Kirill", "Zemnucha"))
    db_cursor.execute("SELECT * FROM actor WHERE first_name = 'Kirill' AND last_name = 'Zemnucha' ")
    result = db_cursor.fetchone()
    assert result is not None, "Newly inserted actor not found"
