import pytest
import requests

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
