import pytest
import requests
import mysql.connector

from ui_tests.constants import API_BASE_URL


@pytest.fixture(scope="session")
def base_url():
    """Fixture for the API base URL."""
    return f"{API_BASE_URL}/actors"


@pytest.fixture(scope="session")
def actor_sample():
    return {"first_name": "John2", "last_name": "Doe2", "last_update": "2006-02-15 04:34:33"}


@pytest.fixture(scope="session")
def actor_integration_sample():
    return {"first_name": "John102", "last_name": "Doe4", "last_update": "2025-01-01 04:34:33"}


@pytest.fixture(scope="session")
def actor_invalid_sample():
    return {"first_name": "", "last_name": "", "last_update": "2025-01-01 04:34:33"}


@pytest.fixture(scope="session")
def film_invalid_data():
    return {

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


@pytest.fixture
def create_actor(base_url):
    """Fixture to create a new actor for testing."""

    def _create_actor(payload):
        response = requests.post(base_url, json=payload)
        response.raise_for_status()
        return response.json()

    return _create_actor


@pytest.fixture(scope="session")
def db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="avitalz",
        database="sakila"
    )
    yield connection
    connection.close()
