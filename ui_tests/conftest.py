import os
import pytest
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture
def db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="avitalz",
        database="sakila"
    )
    yield connection
    connection.close()


def get_browser_options(browser_type):
    if browser_type == "chrome":
        options = ChromeOptions()
    elif browser_type == "firefox":
        options = FirefoxOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser_type}")

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    if os.getenv("CI", "false").lower() == "true":
        options.add_argument("--headless")

    return options


@pytest.fixture(params=["chrome", "firefox"])
def cross_browser_driver(request):
    browser = os.environ.get('BROWSER', request.param).strip().lower()
    options = get_browser_options(browser)

    if browser == "chrome":
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def driver():
    browser = os.environ.get('BROWSER', 'chrome').strip().lower()
    options = get_browser_options(browser)

    if browser == "chrome":
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    yield driver
    driver.quit()
