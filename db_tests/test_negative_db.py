def test_delete_non_existent_film_from_db(db_cursor):
    db_cursor.execute("DELETE FROM film WHERE film_id = 999999")
    assert db_cursor.rowcount == 0, "Expected no rows to be deleted"
