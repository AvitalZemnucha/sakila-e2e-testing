def test_delete_non_existent_film_from_db(db_cursor):
    db_cursor.execute("DELETE FROM film WHERE film_id = 999999")
    deleted_rows = db_cursor.rowcount
    assert deleted_rows == 0, f"Expected 0 rows deleted, but got {deleted_rows}"
