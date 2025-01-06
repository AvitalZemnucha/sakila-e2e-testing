def test_delete_non_existent_film_from_db(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM film WHERE film_id = 999999")
    assert cursor.rowcount == 0, "Expected no rows to be deleted"
