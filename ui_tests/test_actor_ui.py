import os
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


def test_creat_actor(driver):
    driver.get(UI_BASE_URL)
    add_new_actor = driver.find_element(By.XPATH, CREATE_NEW_ACTOR)
    add_new_actor.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, FIRST_NAME_ID))).send_keys("NEW_Actor")
    wait.until(EC.presence_of_element_located((By.ID, LAST_NAME_ID))).send_keys("Last_Name")
    driver.find_element(By.XPATH, NEW_ACTOR_SUBMIT).click()

    driver.refresh()

    wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
    actor_list = driver.find_elements(By.XPATH, ACTOR_LIST)
    last_actor = actor_list[-1]
    for new_actor in actor_list:
        if "NEW_Actor" in new_actor.text:
            last_actor = new_actor
    assert "NEW_Actor" in last_actor.text, "The new actor's first name is not found in the last row."
    assert "Last_Name" in last_actor.text, "The new actor's last name is not found in the last row."


def test_update_actor(driver):
    driver.get(UI_BASE_URL)
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.XPATH, "//tr[@id='actor-1']//button[contains(text(), 'Edit')]").click()
    wait.until(EC.presence_of_element_located((By.ID, EDIT_FIRST_NAME_ID))).clear()
    driver.find_element(By.ID, EDIT_FIRST_NAME_ID).send_keys("AvitalUpdated")
    wait.until(EC.presence_of_element_located((By.ID, EDIT_LAST_NAME_ID))).clear()
    driver.find_element(By.ID, EDIT_LAST_NAME_ID).send_keys("ZemnuchaUpdated")
    driver.find_element(By.XPATH, "//*[@id='edit-form']/button[1]").click()
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
    actor_list = driver.find_elements(By.XPATH, ACTOR_LIST)

    found = False
    for actor in actor_list:
        if "AvitalUpdated" in actor.text and "ZemnuchaUpdated" in actor.text:
            found = True
            break
    assert found, "Actor wasn't updated"


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
