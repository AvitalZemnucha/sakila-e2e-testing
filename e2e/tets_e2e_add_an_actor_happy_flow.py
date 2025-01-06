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

BASE_URL = "http://127.0.0.1:5000/api/actors"
UI_URL = "http://127.0.0.1:5000/"


def test_e2e_adding_delete_actor(driver, db_connection):
    new_actor = {
        "first_name": "Danielle",
        "last_name": "Shaked",
        "last_update": "2006-02-15 04:34:33"
    }
    response = requests.post(BASE_URL, json=new_actor)
    data = response.json()
    assert response.status_code == 201, "New Actor was not created successfully..."
    assert data["first_name"] == "Danielle"

    # UI VERIFICATION
    driver.get(UI_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table//tbody//tr")))
    actor_list = driver.find_elements(By.XPATH, "//table//tbody//tr")
    last_actor = actor_list[-1]
    assert "Danielle" in last_actor.text

    # DELETING ACTOR VIA API
    response = requests.delete(f"{BASE_URL}/{data['id']}")
    assert response.status_code == 204, "Actor was not deleted successfully..."

    # SEARCHING THE DELETED ACTOR IN DB
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM actor WHERE actor_id =%s', (data['id'],))
    result = cursor.fetchone()
    assert result is None, "The actor was not deleted"
    cursor.close()
    db_connection.close()
