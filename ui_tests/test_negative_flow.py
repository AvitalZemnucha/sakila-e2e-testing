import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import (
    UI_BASE_URL,
    ACTOR_LIST,
    CREATE_NEW_ACTOR,
    NEW_ACTOR_SUBMIT,
    FIRST_NAME_ID,
    LAST_NAME_ID,
    EDIT_FIRST_NAME_ID,
    EDIT_LAST_NAME_ID,
    UPDATE_BUTTON
)


def test_add_actor_negative(driver):
    driver.get(UI_BASE_URL)
    wait = WebDriverWait(driver, 10)
    add_new_actor = driver.find_element(By.XPATH, CREATE_NEW_ACTOR)
    add_new_actor.click()
    first_name = wait.until(EC.presence_of_element_located((By.ID, FIRST_NAME_ID)))
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="create-form"]/button'))).click()
    validation_message = driver.execute_script("return arguments[0].validationMessage;", first_name)
    print(validation_message)  # Should print "Please fill out this field"
    assert validation_message == "Please fill out this field."


def test_search_for_non_existing_actor(driver):
    driver.get(UI_BASE_URL)
    table_row = driver.find_elements(By.XPATH, '//*[@id="actor-table-body"]//tr')
    found = False
    for row in table_row:
        if "NICKNICK" not in row.text:
            found = True
            break
    assert found, "Actor not found."


def test_edit_actor(driver):
    driver.get(UI_BASE_URL)
    edit_button = driver.find_element(By.XPATH, "//tr[@id='actor-1']//button[contains(text(), 'Edit')]")
    edit_button.click()
    wait = WebDriverWait(driver, 10)
    first_name = wait.until(EC.presence_of_element_located((By.ID, EDIT_FIRST_NAME_ID)))
    first_name.clear()
    wait.until(EC.presence_of_element_located((By.ID, EDIT_LAST_NAME_ID))).clear()
    update_button = driver.find_element(By.XPATH, UPDATE_BUTTON)
    update_button.click()
    validation_message = driver.execute_script("return arguments[0].validationMessage;", first_name)
    print(validation_message)  # Should print "Please fill out this field"
    assert validation_message == "Please fill out this field."
