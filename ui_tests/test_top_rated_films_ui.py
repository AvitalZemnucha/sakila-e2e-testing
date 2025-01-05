import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL_UI = "http://127.0.0.1:5000/"


def test_top_rated_films_ui(driver):
    driver.get(BASE_URL_UI)
    top_rated_films = driver.find_element(By.XPATH, "//a[@class='nav-link'][2]")
    top_rated_films.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
    result_text = driver.find_element(By.XPATH, "//h1")
    assert "Top Rated Films" in result_text.text
    table_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    film_found = False
    for row in table_rows:
        if "ADAPTATION HOLES" in row.text:
            film_found = True
            break
    assert film_found, "The film 'ADAPTATION HOLES' was not found in the table rows."
