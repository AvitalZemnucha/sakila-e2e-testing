import pytest
import requests
import mysql.connector
import time

from conftest import db_connection

BASE_URL = "http://127.0.0.1:5000/api"


def test_get_actor():
    url = f"{BASE_URL}/actors"
    response = requests.get(url)
    assert response.status_code == 200
    actors = response.json()
    assert len(actors) > 0


def test_create_actor():
    new_actor = {"first_name": "John2", "last_name": "Doe2", "last_update": "2006-02-15 04:34:33"}
    url = f"{BASE_URL}/actors"
    response = requests.post(url, json=new_actor)
    assert response.status_code == 201
    created_actor = response.json()
    assert created_actor["first_name"] == "John2"
    assert created_actor["last_name"] == "Doe2"


def test_create_actor_integration(db_connection):
    new_actor = {"first_name": "John102", "last_name": "Doe4", "last_update": "2025-01-01 04:34:33"}
    url = f"{BASE_URL}/actors"
    response = requests.post(url, json=new_actor)
    assert response.status_code == 201
    created_actor = response.json()
    assert created_actor["first_name"] == "John102"
    assert created_actor["last_name"] == "Doe4"
    new_actor_first_name = created_actor["first_name"]

    cursor = db_connection.cursor()
    cursor.execute(f"SELECT * FROM actor WHERE first_name='{new_actor_first_name}'")
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == "John102"
    assert result[2] == "Doe4"
