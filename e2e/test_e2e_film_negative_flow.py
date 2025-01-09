import pytest
import requests
import mysql.connector
from conftest import db_connection
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui_tests.constants import (
    UI_BASE_URL,
    ACTOR_LIST,
    API_BASE_URL,
    FILM_API_BASE_URL,
    RESUL_TEXT
)


def test_adding_film_with_missing_title(driver):
    url = f"{FILM_API_BASE_URL}"
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

    driver.get(f"{UI_BASE_URL}/top_rated_films?page=23")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, RESUL_TEXT)))
    result_text = driver.find_element(By.XPATH, RESUL_TEXT)
    assert "Top Rated Films" in result_text.text
    table_rows = driver.find_elements(By.XPATH, ACTOR_LIST)
    row_count_before = len(table_rows)
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
    table_rows_after = driver.find_elements(By.XPATH, ACTOR_LIST)
    row_count_after = len(table_rows_after)
    assert row_count_before == row_count_after, "The table row count changed unexpectedly after a failed film creation."
