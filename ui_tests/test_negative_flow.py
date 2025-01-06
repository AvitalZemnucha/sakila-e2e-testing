import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL_UI = "http://127.0.0.1:5000/"


def test_add_actor_negative(driver):
    driver.get(BASE_URL_UI)
    wait = WebDriverWait(driver, 10)
    add_new_actor = driver.find_element(By.XPATH, "//button[contains(text(), 'New')]")
    add_new_actor.click()
    first_name = wait.until(EC.presence_of_element_located((By.ID, "create-firstName")))
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="create-form"]/button'))).click()
    validation_message = driver.execute_script("return arguments[0].validationMessage;", first_name)
    print(validation_message)  # Should print "Please fill out this field"
    assert validation_message == "Please fill out this field."


def test_search_for_non_existing_actor(driver):
    driver.get(BASE_URL_UI)

    table_row = driver.find_elements(By.XPATH, '//*[@id="actor-table-body"]//tr')
    found = False
    for row in table_row:
        if "NICKNICK" not in row.text:
            found = True
            break
    assert found, "Actor not found."


def test_edit_actor(driver):
    driver.get(BASE_URL_UI)
    edit_button = driver.find_element(By.XPATH, "//button[@data-id='1']")
    edit_button.click()
    wait = WebDriverWait(driver, 10)
    first_name = wait.until(EC.presence_of_element_located((By.ID, "edit-firstName")))
    first_name.clear()
    wait.until(EC.presence_of_element_located((By.ID, "edit-lastName"))).clear()
    update_button = driver.find_element(By.XPATH, "//*[@id='edit-form']/button")
    update_button.click()
    validation_message = driver.execute_script("return arguments[0].validationMessage;", first_name)
    print(validation_message)  # Should print "Please fill out this field"
    assert validation_message == "Please fill out this field."
