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

BASE_URL = "http://127.0.0.1:5000/api/"
UI_URL = "http://127.0.0.1:5000/"


def test_add_actor_with_invalid_first_name(driver):
    url = f"{BASE_URL}/actors"
    new_actor = {
        "first_name": '',
        "last_name": '',
        "last_update": "2006-02-15 04:34:33"
    }
    response = requests.post(url, json=new_actor)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert "First name and last name are required" in response.json()['error']
    driver.get(UI_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table//tbody//tr")))
    actor_list = driver.find_elements(By.XPATH, "//table//tbody//tr")
    last_actor = actor_list[-1]
    assert "Danielle" not in last_actor.text
