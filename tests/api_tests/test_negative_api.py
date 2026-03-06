import pytest
import requests
from config_data import (API_BASE_URL, INVALID_FILM_DATA)


def test_add_actor_with_invalid_first_name(actor_invalid_sample, api_actors_url):
    response = requests.post(api_actors_url, json=actor_invalid_sample)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    error_msg = response.json().get('error', '')
    assert "First name and last name are required" in error_msg


def test_add_invalid_test_data(film_invalid_data):
    url = f"{API_BASE_URL}/films"
    response = requests.post(url, json=film_invalid_data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    error_msg = response.json().get('error', '')
    assert "Title is required" in error_msg
