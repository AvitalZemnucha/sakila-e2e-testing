import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def test_cross_browsers(cross_browser_driver):
    print(f"Running test on browser: {cross_browser_driver.name}")
    url = "http://127.0.0.1:5000/"
    cross_browser_driver.get(url)
    actor_list = cross_browser_driver.find_elements(By.XPATH, "//table//tbody//tr")
    assert len(actor_list) > 0, "No actor list"
    assert actor_list[0].is_displayed(), "No actor list"
