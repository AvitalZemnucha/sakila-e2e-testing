import pytest
import requests
from conftest import db_connection
from config_data import (
    API_BASE_URL
)


def test_get_actor(api_actors_url):
    response = requests.get(api_actors_url)
    assert response.status_code == 200
    actors = response.json()
    assert len(actors) > 0


def test_create_actor_with_faker(api_actors_url, actor_sample):
    url = api_actors_url
    response = requests.post(url, json=actor_sample)
    assert response.status_code == 201
    created_actor = response.json()
    assert created_actor["first_name"] == actor_sample["first_name"]
    assert created_actor["last_name"] == actor_sample["last_name"]


def test_create_actor_integration_api_db(db_cursor, api_actors_url, actor_sample, create_actor):
    # Create actor using faker
    created_actor = create_actor(actor_sample)

    # Assertions for API response
    assert created_actor["first_name"] == actor_sample["first_name"]
    assert created_actor["last_name"] == actor_sample["last_name"]

    query = "SELECT first_name, last_name FROM actor WHERE first_name = %s AND last_name = %s"
    db_cursor.execute(query, (actor_sample["first_name"], actor_sample["last_name"]))
    result = db_cursor.fetchone()

    assert result is not None, f"Actor {actor_sample['first_name']} not found in DB"
    assert result["first_name"] == actor_sample["first_name"]
