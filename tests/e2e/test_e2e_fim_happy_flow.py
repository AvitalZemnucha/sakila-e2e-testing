# tests/e2e/test_e2e_film_happy_flow.py
import requests
import pytest
from tests.base_test import BaseTest
from pages.film_page import FilmPage
from config_data import FILM_API_BASE_URL

NEW_FILM_PAYLOAD = {
    "title": "NEW YEAR 2025",
    "description": "SyFy film about blabla",
    "release_year": "2025",
    "language_id": "1",
    "rental_duration": "3",
    "rental_rate": "2.99",
    "length": "182",
    "replacement_cost": "19.99",
    "rating": "PG",
    "special_features": "Deleted Scenes"
}


class TestFilmHappyFlowE2E(BaseTest):
    film_page: FilmPage

    def test_film_full_lifecycle(self, db_connection):
        """
        E2E Happy Flow — full film lifecycle:
        1. CREATE  : POST film via API → assert 201 + DB record exists.
        2. UPDATE  : PUT rating change  → assert 200 + fields correct.
        3. VERIFY  : GET film by id     → assert title persisted.
        4. DELETE  : DELETE film        → assert 204 + 404 on re-fetch.
        5. DB CHECK: confirm row gone from database.
        6. UI CHECK: confirm film absent from Top Rated Films table.
        """

        # ── Step 1: CREATE ────────────────────────────────────────────
        response = requests.post(FILM_API_BASE_URL, json=NEW_FILM_PAYLOAD)
        assert response.status_code == 201, (
            f"Expected 201 Created, got {response.status_code}: {response.json()}"
        )
        film_id = response.json()["id"]

        cursor = db_connection.cursor()
        cursor.execute("SELECT film_id, title FROM film ORDER BY film_id DESC LIMIT 1")
        db_film_id, db_title = cursor.fetchone()
        assert "NEW YEAR 2025" in db_title, (f"Film not found in DB. Latest title: '{db_title}'")
        assert film_id == db_film_id, (f"API id {film_id} does not match DB id {db_film_id}")

        # ── Step 2: UPDATE ────────────────────────────────────────────
        response = requests.put(f"{FILM_API_BASE_URL}/{film_id}", json={"rating": "NC-17"})
        assert response.status_code == 200, (f"Expected 200 OK on update, got {response.status_code}")
        updated = response.json()
        assert updated["title"] == "NEW YEAR 2025"
        assert updated["rating"] == "NC-17", (f"Rating not updated. Got: '{updated['rating']}'")

        # ── Step 3: VERIFY ────────────────────────────────────────────
        response = requests.get(f"{FILM_API_BASE_URL}/{film_id}")
        assert response.status_code == 200, (f"Expected 200 on GET after update, got {response.status_code}")
        assert response.json()["title"] == "NEW YEAR 2025"

        # ── Step 4: DELETE ────────────────────────────────────────────
        response = requests.delete(f"{FILM_API_BASE_URL}/{film_id}")
        assert response.status_code == 204, (f"Expected 204 No Content on delete, got {response.status_code}")
        response = requests.get(f"{FILM_API_BASE_URL}/{film_id}")
        assert response.status_code == 404, (f"Expected 404 after deletion, got {response.status_code}")

        # ── Step 5: DB CHECK ──────────────────────────────────────────
        cursor.execute("SELECT * FROM film WHERE film_id = %s", (film_id,))
        assert cursor.fetchone() is None, (f"Film id {film_id} still exists in the database after deletion.")

        # ── Step 6: UI CHECK ──────────────────────────────────────────
        self.film_page.open_last_page()
        assert not self.film_page.is_text_present_in_table("NEW YEAR 2025"), (
            "Deleted film 'NEW YEAR 2025' still appears in the Top Rated Films table."
            )
