import pytest
import requests
import mysql.connector
import time

from conftest import db_connection

BASE_URL = "http://127.0.0.1:5000/api/"


def test_add_actor_with_invalid_first_name():
    url = f"{BASE_URL}/actors"
    new_actor = {
        "first_name": '',
        "last_name": '',
        "last_update": "2006-02-15 04:34:33"
    }
    response = requests.post(url, json=new_actor)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert "First name and last name are required" in response.json()['error']


def test_add_invalid_test_data():
    url = f"{BASE_URL}/films"
    new_film = {

        "description": 'A Fast+Paced Documentary',
        "release_year": '2025',
        "language_id": '1',  # Default to 1 if not provided
        "rental_duration": '6',
        "rental_rate": '4.99',
        "length": '180',
        "replacement_cost": '19.99',
        "rating": 'PG-13',
        "special_features": 'Deleted Scenes'
    }

    response = requests.post(url, json=new_film)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert "Title is required" in response.json()['error']
