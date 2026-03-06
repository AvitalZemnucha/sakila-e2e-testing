import pytest


def test_actor_count(db_cursor):
    db_cursor.execute("SELECT COUNT(*) AS total FROM actor")
    result = db_cursor.fetchone()
    assert result['total'] > 0


def test_actor_names(db_cursor):
    db_cursor.execute("SELECT last_name, first_name FROM actor LIMIT 5")
    result = db_cursor.fetchall()
    assert len(result) == 5
    for row in result:
        assert len(row["first_name"]) > 0 and len(row["last_name"]) > 0


def test_actor_insertion_using_faker(db_cursor, actor_sample):
    f_name = actor_sample['first_name']
    l_name = actor_sample['last_name']
    insert_query = "INSERT INTO actor (first_name, last_name) VALUES (%s, %s)"
    db_cursor.execute(insert_query, (f_name, l_name))

    select_query = "SELECT * FROM actor WHERE first_name = %s AND last_name = %s"
    db_cursor.execute(select_query, (f_name, l_name))
    result = db_cursor.fetchone()

    assert result is not None, f"Actor {f_name} {l_name} was not inserted correctly"
    assert result['first_name'] == f_name
    assert result['last_name'] == l_name

    db_cursor.execute("DELETE FROM actor WHERE first_name = %s AND last_name = %s", (f_name, l_name))
