import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageChops
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


def test_visual_regression(driver):
    driver.get(UI_BASE_URL)
    driver.save_screenshot("before.png")
    add_new_actor = driver.find_element(By.XPATH, CREATE_NEW_ACTOR)
    add_new_actor.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, FIRST_NAME_ID))).send_keys("NEW_Actor_for_regression")
    wait.until(EC.presence_of_element_located((By.ID, LAST_NAME_ID))).send_keys("Last_Name_for_regression")
    driver.find_element(By.XPATH, NEW_ACTOR_SUBMIT).click()

    driver.refresh()

    wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    actor_list = driver.find_elements(By.XPATH, ACTOR_LIST)
    last_actor = actor_list[-1]
    for new_actor in actor_list:
        if "NEW_Actor_for_regression" in new_actor.text:
            last_actor = new_actor
    assert "NEW_Actor_for_regression" in last_actor.text, "The new actor's first name is not found in the last row."
    assert "Last_Name_for_regression" in last_actor.text, "The new actor's last name is not found in the last row."
    driver.save_screenshot("after.png")

    before_img = Image.open("before.png")
    after_img = Image.open("after.png")
    diff = ImageChops.difference(before_img, after_img)

    assert diff.getbbox() is not None
