import pytest
import requests
import mysql.connector
import time

from conftest import db_connection

BASE_URL = "http://127.0.0.1:5000/api/films"


def test_get_top_rated():
    url = f"{BASE_URL}/top_rated"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert type(data) == dict
    assert len(data) > 0
