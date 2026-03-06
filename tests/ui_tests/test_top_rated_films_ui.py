# test_top_rated_films_ui.py
import pytest
from tests.base_test import BaseTest
from pages.film_page import FilmPage


class TestFilmsUI(BaseTest):
    film_page: FilmPage

    def test_top_rated_films_ui(self):
        self.film_page.open_top_rated()

        loaded = self.film_page.wait_for_results_to_load()
        assert loaded, "The films page did not load correctly."

        assert self.film_page.is_top_rated_header_correct(), "Header text mismatch!"

        film_found = self.film_page.is_text_present_in_table("ADAPTATION HOLES")
        assert film_found, "The film 'ADAPTATION HOLES' was not found in the table."
