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

from ui_tests.test_top_rated_films_ui import BASE_URL_UI

BASE_URL = "http://127.0.0.1:5000/api/films"


def test_adding_film_with_missing_title(driver):
    url = f"{BASE_URL}"
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

    driver.get(f"{BASE_URL_UI}/top_rated_films?page=23")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
    result_text = driver.find_element(By.XPATH, "//h1")
    assert "Top Rated Films" in result_text.text
    table_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    row_count_before = len(table_rows)
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr")))
    table_rows_after = driver.find_elements(By.XPATH, "//table/tbody/tr")
    row_count_after = len(table_rows_after)
    assert row_count_before == row_count_after, "The table row count changed unexpectedly after a failed film creation."
