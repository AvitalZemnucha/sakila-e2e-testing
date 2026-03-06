import pytest
import requests
from config_data import FILM_API_BASE_URL


def test_get_top_rated_films():
    url = f"{FILM_API_BASE_URL}/top_rated"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    data = response.json()
    assert isinstance(data, dict), "Response should be a dictionary"
    assert type(data) == dict
    assert len(data) > 0, "Top rated list is empty"

    if "top_films" in data:
        first_film = data["top_films"][0]
        assert "title" in first_film, "Film object missing 'title' field"
        assert "rental_rate" in first_film or "rating" in first_film, "Film object missing rating info"
