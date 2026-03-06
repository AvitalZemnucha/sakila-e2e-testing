import os
import pytest
import mysql.connector
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from faker import Faker
from config_data import API_BASE_URL, INVALID_ACTOR_DATA, INVALID_FILM_DATA
from pages.actor_page import ActorPage
from dotenv import load_dotenv

load_dotenv()


# --- DATABASE FIXTURES ---
@pytest.fixture(scope="session")
def db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "avitalz"),
        database=os.getenv("DB_NAME", "sakila"),
        autocommit=True  # always reads current DB state — no manual commit() needed
    )
    yield connection
    connection.close()


@pytest.fixture
def db_cursor(db_connection):
    cursor = db_connection.cursor(dictionary=True)
    yield cursor
    cursor.close()


# --- BROWSER / UI FIXTURES ---
def get_browser_options(browser_type: str):
    options_map = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "edge": EdgeOptions(),
    }
    if browser_type not in options_map:
        raise ValueError(f"Unsupported browser: {browser_type}")
    options = options_map[browser_type]
    options.add_argument("--window-size=1920,1080")
    if os.getenv("CI", "false").lower() == "true":
        options.add_argument("--headless")
    return options


@pytest.fixture(params=["chrome", "firefox", "edge"], scope="function")
def driver(request):
    browser = request.param
    options = get_browser_options(browser)

    if browser == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        drv = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        drv = webdriver.Firefox(service=service, options=options)

    elif browser == "edge":
        possible_paths = [
            os.path.join(os.getcwd(), "msedgedriver.exe"),
            os.path.join(os.path.dirname(__file__), "msedgedriver.exe"),
            os.path.join(os.path.dirname(__file__), "drivers", "msedgedriver.exe"),
        ]
        local_path = next((p for p in possible_paths if os.path.exists(p)), None)

        if local_path:
            print(f"\n[Edge] Using local driver found at: {local_path}")
            drv = webdriver.Edge(service=EdgeService(executable_path=local_path), options=options)
        else:
            print("\n[Edge] Local driver not found, attempting auto-download...")
            try:
                drv = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
            except Exception as e:
                pytest.fail(
                    f"[Edge] Both local lookup and auto-download failed.\n"
                    f"Searched paths: {possible_paths}\n"
                    f"Error: {e}"
                )

    yield drv
    drv.quit()


@pytest.fixture
def actor_page(driver):
    return ActorPage(driver)


# --- API FIXTURES ---
@pytest.fixture(scope="session")
def api_actors_url():
    return f"{API_BASE_URL}/actors"


@pytest.fixture
def actor_sample():
    fake = Faker()
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "last_update": "2006-02-15 04:34:33"
    }


@pytest.fixture
def create_actor(api_actors_url):
    def _create(payload):
        response = requests.post(api_actors_url, json=payload)
        response.raise_for_status()
        return response.json()

    return _create


@pytest.fixture
def actor_invalid_sample():
    return INVALID_ACTOR_DATA


@pytest.fixture
def film_invalid_data():
    return INVALID_FILM_DATA
