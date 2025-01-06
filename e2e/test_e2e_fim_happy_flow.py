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


def test_e2e1(driver, db_connection):
    new_film = {
        "title": "NEW YEAR 2025",
        "description": "SyFy film about blabla",
        "release_year": "2025",
        "language_id": "1",
        "rental_duration": "3",
        "rental_rate": "2.99",
        "length": "182",
        "replacement_cost": "19.99",
        "rating": "PG",
        "special_features": "Deleted Scenes"
    }
    response = requests.post(BASE_URL, json=new_film)
    data = response.json()
    assert response.status_code == 201, "Expected 201 status code"
    data_film_id = data["id"]
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM film ORDER BY film_id DESC LIMIT 1')
    result = cursor.fetchone()
    last_film = result[1]
    last_fil_id = result[0]
    assert "NEW YEAR 2025" in last_film

    if data_film_id == last_fil_id:
        update_film_rating = {"rating": "NC-17"}
        response = requests.put(f"{BASE_URL}/{data_film_id}", json=update_film_rating)
        data = response.json()
        assert response.status_code == 200, "Expected 200 status code"
        assert data["title"] == "NEW YEAR 2025"
        assert data["rating"] == "NC-17"

    # response = requests.get(f"{BASE_URL}/top_rated")
    # data = response.json()
    # assert response.status_code == 200, "Expected 200 status code"
    #
    # found = False
    # for film in data['films']:
    #     if film["id"] == data_film_id:
    #         found = True
    #         break
    # assert found == True
    response = requests.get(f"{BASE_URL}/{data_film_id}")
    data_update = response.json()
    assert response.status_code == 200, "Expected 200 status code"
    assert data_update["title"] == "NEW YEAR 2025"

    # Delete Film
    response_delete = requests.delete(f"{BASE_URL}/{data_film_id}")
    assert response_delete.status_code == 204, "Expected 204 status code"
    response = requests.get(f"{BASE_URL}/{data_film_id}")
    assert response.status_code == 404, "Expected 404 status code"

    # Verify that film was deleted from DB
    new_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="avitalz",
        database="sakila"
    )
    new_cursor = new_connection.cursor()
    new_cursor.execute("SELECT * FROM film WHERE film_id = %s", (data_film_id,))
    result = new_cursor.fetchone()
    assert result is None, "The film was not deleted from the database."
    new_cursor.close()
    new_connection.close()

    # UI check that the film was deleted
    driver.get(f"{BASE_URL_UI}/top_rated_films?page=23")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
    result_text = driver.find_element(By.XPATH, "//h1")
    assert "Top Rated Films" in result_text.text
    table_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    film_found = True
    for row in table_rows:
        if "NEW YEAR 2025" in row.text:
            film_found = False
            break
    assert film_found, "The film 'NEW YEAR 2025' was found in the table rows."
