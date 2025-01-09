import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from constants import (
    UI_BASE_URL,
    ACTOR_LIST
)


def test_cross_browsers(cross_browser_driver):
    print(f"Running test on browser: {cross_browser_driver.name}")
    cross_browser_driver.get(UI_BASE_URL)
    actor_list = cross_browser_driver.find_elements(By.XPATH, ACTOR_LIST)
    assert len(actor_list) > 0, "No actor list"
    assert actor_list[0].is_displayed(), "No actor list"
