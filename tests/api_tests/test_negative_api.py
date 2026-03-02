import pytest
import requests
import mysql.connector
import time

from conftest import db_connection
from config_data import (
    API_BASE_URL
)


def test_add_actor_with_invalid_first_name(actor_invalid_sample):
    url = base_url()
    response = requests.post(url, json=actor_invalid_sample)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert "First name and last name are required" in response.json()['error']


def test_add_invalid_test_data(film_invalid_data):
    url = f"{API_BASE_URL}/films"
    response = requests.post(url, json=film_invalid_data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert "Title is required" in response.json()['error']
