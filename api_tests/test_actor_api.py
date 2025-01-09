import pytest
import requests
import mysql.connector
import time

from conftest import db_connection
from ui_tests.constants import (
    API_BASE_URL
)


def test_get_actor(base_url):
    response = requests.get(base_url)
    assert response.status_code == 200
    actors = response.json()
    assert len(actors) > 0


def test_create_actor(base_url, actor_sample):
    url = f"{API_BASE_URL}/actors"
    response = requests.post(url, json=actor_sample)
    assert response.status_code == 201
    created_actor = response.json()
    assert created_actor["first_name"] == "John2"
    assert created_actor["last_name"] == "Doe2"


def test_create_actor_integration(db_connection, base_url, actor_integration_sample, create_actor):
    # Create actor using fixture
    created_actor = create_actor(actor_integration_sample)

    # Assertions for API response
    assert created_actor["first_name"] == actor_integration_sample["first_name"]
    assert created_actor["last_name"] == actor_integration_sample["last_name"]

    cursor = db_connection.cursor()
    cursor.execute(f"SELECT * FROM actor WHERE first_name='{created_actor['first_name']}'")
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == actor_integration_sample["first_name"]
    assert result[2] == actor_integration_sample["last_name"]
