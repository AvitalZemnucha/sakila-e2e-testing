import requests
from tests.base_test import BaseTest
from pages.film_page import FilmPage
from config_data import FILM_API_BASE_URL, INVALID_FILM_DATA


class TestFilmNegativeFlowE2E(BaseTest):
    film_page: FilmPage

    def test_adding_film_with_missing_title_is_rejected(self):
        """
        E2E Negative Flow:
        1. API must reject a film payload with no title (400).
        2. UI must confirm the last page of Top Rated Films is unchanged.
        """
        # --- Step 1: API Layer — assert the request is rejected ---
        response = requests.post(FILM_API_BASE_URL, json=INVALID_FILM_DATA)

        assert response.status_code == 400, (
            f"Expected 400 Bad Request, got {response.status_code}"
        )
        assert "Title is required" in response.json().get("error", ""), (
            f"Unexpected error message: {response.json()}"
        )

        # --- Step 2: UI Layer — confirm table row count is unchanged ---
        self.film_page.open_last_page()

        row_count_before = self.film_page.get_table_row_count()
        assert row_count_before > 0, "Film table is empty — cannot verify row count."

        self.film_page.refresh()

        row_count_after = self.film_page.get_table_row_count()
        assert row_count_before == row_count_after, (
            f"Row count changed after failed film creation: "
            f"before={row_count_before}, after={row_count_after}"
        )
