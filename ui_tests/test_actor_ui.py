import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from constants import (
    UI_BASE_URL,
    ACTOR_LIST,
    CREATE_NEW_ACTOR,
    NEW_ACTOR_SUBMIT,
    FIRST_NAME_ID,
    LAST_NAME_ID,
    EDIT_FIRST_NAME_ID,
    EDIT_LAST_NAME_ID
)


def test_actor_list_page(driver):
    driver.get(UI_BASE_URL)
    actor_list = driver.find_elements(By.XPATH, ACTOR_LIST)
    assert len(actor_list) > 0, "No actor list"
    assert actor_list[0].is_displayed(), "No actor list"


@pytest.mark.parametrize("first_name, last_name", [
    ("NEW_Actor", "Last_Name"),
    ("John", "Doe"),
    ("QA_Test", "User"),
])
def test_create_actor(driver, first_name, last_name):
    driver.get(UI_BASE_URL)
    add_new_actor = driver.find_element(By.XPATH, CREATE_NEW_ACTOR)
    add_new_actor.click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, FIRST_NAME_ID))).send_keys(first_name)
    wait.until(EC.presence_of_element_located((By.ID, LAST_NAME_ID))).send_keys(last_name)
    driver.find_element(By.XPATH, NEW_ACTOR_SUBMIT).click()

    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
    actor_list = driver.find_elements(By.XPATH, ACTOR_LIST)

    found = any(first_name in actor.text and last_name in actor.text for actor in actor_list)
    assert found, f"Actor '{first_name} {last_name}' was not found in the list."


@pytest.mark.parametrize("new_first_name, new_last_name", [
    ("AvitalUpdated", "ZemnuchaUpdated"),
    ("UpdatedJohn", "UpdatedDoe"),
    ("RenamedQA", "RenamedUser"),
])
def test_update_actor(driver, new_first_name, new_last_name):
    driver.get(UI_BASE_URL)
    wait = WebDriverWait(driver, 10)

    # Click edit on actor with id=1 (adjust if needed)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//tr[@id='actor-1']//button[contains(text(), 'Edit')]"))).click()

    first_name_input = wait.until(EC.presence_of_element_located((By.ID, EDIT_FIRST_NAME_ID)))
    first_name_input.clear()
    first_name_input.send_keys(new_first_name)

    last_name_input = wait.until(EC.presence_of_element_located((By.ID, EDIT_LAST_NAME_ID)))
    last_name_input.clear()
    last_name_input.send_keys(new_last_name)

    driver.find_element(By.XPATH, "//*[@id='edit-form']/button[1]").click()
    wait.until(EC.text_to_be_present_in_element((By.XPATH, "//tr[@id='actor-1']"), new_first_name))
    driver.refresh()

    wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
    actor_list = driver.find_elements(By.XPATH, ACTOR_LIST)

    found = any(new_first_name in actor.text and new_last_name in actor.text for actor in actor_list)

    assert found, f"Updated actor '{new_first_name} {new_last_name}' was not found."


def test_delete_actor(driver):
    driver.get(UI_BASE_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
    actor_list = driver.find_elements(By.XPATH, ACTOR_LIST)
    last_actor = actor_list[-1]
    delete_button = last_actor.find_element(By.XPATH, ".//td[4]/button[2]")
    delete_button.click()
    wait.until(EC.alert_is_present())
    Alert(driver).accept()
    wait.until(EC.staleness_of(last_actor))
    driver.refresh()

    actor_list_after_delete = driver.find_elements(By.XPATH, ACTOR_LIST)
    assert len(actor_list_after_delete) == len(actor_list) - 1, "The last actor was not deleted."
