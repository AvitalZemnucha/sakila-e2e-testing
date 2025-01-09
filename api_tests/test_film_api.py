import pytest
import requests
import mysql.connector
import time

from conftest import db_connection
from ui_tests.constants import (
    FILM_API_BASE_URL
)


def test_get_top_rated():
    url = f"{FILM_API_BASE_URL}/top_rated"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert type(data) == dict
    assert len(data) > 0
