import pytest
import mysql.connector


def test_film_count(db_cursor):
    db_cursor.execute('SELECT COUNT(*) AS total FROM film')
    result = db_cursor.fetchone()
    assert result['total'] > 0


def test_title_retrieval(db_cursor):
    db_cursor.execute('SELECT title FROM film')
    results = db_cursor.fetchall()
    assert len(results) >= 1000
    assert results[-1]['title'] is not None


def test_specific_film_title(db_cursor):
    db_cursor.execute('SELECT title FROM film WHERE film_id = 1000')
    result = db_cursor.fetchone()
    assert result is not None, "Film with ID 1000 not found"
    assert "ZORRO ARK" in result['title']


def test_films_have_language(db_cursor):
    query = """
    SELECT f.title, l.name AS language 
    FROM film f 
    JOIN language l ON f.language_id = l.language_id 
    LIMIT 5
    """
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    for row in results:
        assert row['language'] is not None
        print(f"Film: {row['title']} is in {row['language']}")
