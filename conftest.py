import os
import pytest
import mysql.connector
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config_data import API_BASE_URL
from pages.actor_page import ActorPage


# --- DATABASE FIXTURES ---
@pytest.fixture(scope="session")
def db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="avitalz",  # החליפי לסיסמה החדשה כשתסיימי
        database="sakila"
    )
    yield connection
    connection.close()


@pytest.fixture
def db_cursor(db_connection):
    cursor = db_connection.cursor(dictionary=True)  # עבודה עם מילון מקלה על ה-Refactoring
    yield cursor
    cursor.close()


# --- BROWSER / UI FIXTURES ---
def get_browser_options(browser_type):
    if browser_type == "chrome":
        options = ChromeOptions()
    elif browser_type == "firefox":
        options = FirefoxOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser_type}")

    options.add_argument("--window-size=1920,1080")
    if os.getenv("CI", "false").lower() == "true":
        options.add_argument("--headless")
    return options


@pytest.fixture(scope="function")
def driver():
    browser = os.environ.get('BROWSER', 'chrome').strip().lower()
    options = get_browser_options(browser)
    driver = webdriver.Chrome(options=options) if browser == "chrome" else webdriver.Firefox(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def actor_page(driver):
    return ActorPage(driver)


# --- API FIXTURES ---
@pytest.fixture(scope="session")
def base_url():
    return f"{API_BASE_URL}/actors"


@pytest.fixture
def actor_sample():
    return {"first_name": "John", "last_name": "Doe", "last_update": "2006-02-15 04:34:33"}


@pytest.fixture
def create_actor(api_actors_url):
    def _create(payload):
        response = requests.post(api_actors_url, json=payload)
        response.raise_for_status()
        return response.json()

    return _create
