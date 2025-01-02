import os
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--disable-gpu")  # Disables GPU rendering
    options.add_argument("--no-sandbox")  # Recommended for Jenkins
    options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues
    options.add_argument("--window-size=1920,1080")  # Optional: Define browser size
    # Enable headless mode only in Jenkins
    if os.getenv("CI", "false").lower() == "true":
        options.add_argument("--headless")
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_actor_list_page(driver):
    url = "http://127.0.0.1:5000/"
    driver.get(url)
    actor_list = driver.find_elements(By.XPATH, "//table//tbody//tr")
    assert len(actor_list) > 0, "No actor list"
    assert actor_list[0].is_displayed(), "No actor list"


def test_creat_actor(driver):
    url = "http://127.0.0.1:5000/"
    driver.get(url)
    add_new_actor = driver.find_element(By.XPATH, "//button[contains(text(), 'New')]")
    add_new_actor.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "create-first-name"))).send_keys("NEW_Actor")
    wait.until(EC.presence_of_element_located((By.ID, "create-last-name"))).send_keys("Last_Name")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody//tr")))
    actor_list = driver.find_elements(By.XPATH, "//table//tbody//tr")
    last_actor = actor_list[-1]
    assert "NEW_Actor" in last_actor.text, "The new actor's first name is not found in the last row."
    assert "Last_Name" in last_actor.text, "The new actor's last name is not found in the last row."


def test_update_actor(driver):
    url = "http://127.0.0.1:5000/"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.XPATH, "//button[@data-id='216']").click()
    wait.until(EC.presence_of_element_located((By.ID, "edit-first-name"))).clear()
    driver.find_element(By.ID, "edit-first-name").send_keys("AvitalUpdated")
    wait.until(EC.presence_of_element_located((By.ID, "edit-last-name"))).clear()
    driver.find_element(By.ID, "edit-last-name").send_keys("ZemnuchaUpdated")
    driver.find_element(By.XPATH, "//*[@id='edit-form']/button[1]").click()
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody//tr")))
    actor_list = driver.find_elements(By.XPATH, "//table//tbody//tr")

    found = False
    for actor in actor_list:
        if "AvitalUpdated" in actor.text and "ZemnuchaUpdated" in actor.text:
            found = True
            break
    assert found, "Actor wasn't updated"


def test_delete_actor(driver):
    url = "http://127.0.0.1:5000/"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody//tr")))
    actor_list = driver.find_elements(By.XPATH, "//table//tbody//tr")
    last_actor = actor_list[-1]
    delete_button = last_actor.find_element(By.XPATH, ".//td[4]/button[2]")
    delete_button.click()
    wait.until(EC.alert_is_present())
    Alert(driver).accept()
    wait.until(EC.staleness_of(last_actor))
    driver.refresh()

    actor_list_after_delete = driver.find_elements(By.XPATH, "//table//tbody//tr")
    assert len(actor_list_after_delete) == len(actor_list) - 1, "The last actor was not deleted."
