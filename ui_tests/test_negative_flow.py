import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert

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


@pytest.mark.parametrize("first_name,last_name,missing_field_id", [
    ("", "Smith", FIRST_NAME_ID),
    ("John", "", LAST_NAME_ID),
    ("", "", FIRST_NAME_ID),  # Prioritize checking the first missing field
])
def test_add_actor_negative_parametrized(driver, first_name, last_name, missing_field_id):
    driver.get(UI_BASE_URL)
    wait = WebDriverWait(driver, 10)
    # Click "Add New Actor"
    driver.find_element(By.XPATH, CREATE_NEW_ACTOR).click()
    # Fill fields if data provided
    if first_name:
        driver.find_element(By.ID, FIRST_NAME_ID).send_keys(first_name)
    if last_name:
        driver.find_element(By.ID, LAST_NAME_ID).send_keys(last_name)
    # Try to submit the form
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="create-form"]/button')))
    submit_button.click()
    # Check validation message
    missing_field = driver.find_element(By.ID, missing_field_id)
    validation_message = driver.execute_script("return arguments[0].validationMessage;", missing_field)
    assert validation_message == "Please fill out this field.", f"Expected validation message on field: {missing_field_id}"


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


@pytest.mark.parametrize("new_first_name,new_last_name,expected_error_type,reason", [
    ("", "UpdatedLast", "validation", "Empty first name"),
    ("UpdatedFirst", "", "validation", "Empty last name"),
    ("", "", "validation", "Both fields empty"),
    ("A" * 100, "UpdatedLast", "alert", "Too long first name"),
    ("UpdatedFirst", "B" * 100, "alert", "Too long last name"),
])
def test_edit_actor_negative_parametrized(driver, new_first_name, new_last_name, expected_error_type, reason):
    driver.get(UI_BASE_URL)
    wait = WebDriverWait(driver, 10)
    # Go to edit form
    edit_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//tr[@id='actor-1']//button[contains(text(), 'Edit')]")))
    edit_button.click()
    # Clear and enter values
    first_name_input = wait.until(EC.presence_of_element_located((By.ID, EDIT_FIRST_NAME_ID)))
    first_name_input.clear()
    last_name_input = wait.until(EC.presence_of_element_located((By.ID, EDIT_LAST_NAME_ID)))
    last_name_input.clear()

    if new_first_name:
        first_name_input.send_keys(new_first_name)
    if new_last_name:
        last_name_input.send_keys(new_last_name)
    # Submit form
    driver.find_element(By.XPATH, UPDATE_BUTTON).click()
    try:
        if expected_error_type == "validation":
            field = first_name_input if not new_first_name.strip() else last_name_input
            validation_message = driver.execute_script("return arguments[0].validationMessage;", field)
            assert validation_message == "Please fill out this field.", f"[{reason}] Missing expected validation"
        elif expected_error_type == "alert":
            # Wait for the alert to appear
            alert = wait.until(EC.alert_is_present())
            assert "Error updating actor" in alert.text, f"[{reason}] Alert text mismatch"
            alert.accept()
    except UnexpectedAlertPresentException:
        alert = Alert(driver)
        assert "Error updating actor" in alert.text, f"[{reason}] Unexpected alert content"
        alert.accept()
