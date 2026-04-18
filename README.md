# Sakila E2E Test Automation Project

This project provides a full-stack end-to-end testing solution for the Sakila Sample Database application. It includes a
Python Flask web application and a comprehensive test suite covering **UI (Selenium)**, **API (Requests)**, and *
*Database (SQLAlchemy)** testing.

## 🚀 Project Architecture

The project follows the **Page Object Model (POM)** pattern for UI tests and uses a centralized `conftest.py` for shared
fixtures.

* **App:** Flask (Python)
* **Testing Framework:** Pytest
* **UI Automation:** Selenium WebDriver
* **API Testing:** Requests
* **Database Testing:** SQLAlchemy / PyMySQL
* **Data Generation:** Faker

---

## 🛠️ Setup and Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
cd sakila-e2e-testing

```

2. **Create a Virtual Environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt

```

---

## 🏃 Running the Application

Before running any tests, the local server and database connection must be active.

1. **Start the Flask App:**

```bash
python app.py

```

2. The app will be available at: `http://127.0.0.1:5000`

---

## 🧪 Executing Tests

The project is organized into sub-packages under the `tests/` directory. You can run all tests or specific suites.

### Run All Tests

```bash
pytest

```

### Cross-Browser UI Execution

* **Run only on Chrome:** `pytest tests/ui_tests -k "chrome"`
* **Run only on Firefox:** `pytest tests/ui_tests -k "firefox"`
* **Run only on Edge:** `pytest tests/ui_tests -k "edge"`
* **Run all browsers with logs visible (shows browser names)::** `pytest tests/ui_tests -s`

### Run Specific Test Suites

* **UI Tests:** `pytest tests/ui_tests`
* **API Tests:** `pytest tests/api_tests`
* **Database Tests:** `pytest tests/db_tests`
* **E2E (End-to-End) Flows:** `pytest tests/e2e`

### Generate HTML Report

```bash
pytest --html=reports/report.html --self-contained-html

```

---

## 📁 Project Structure

```text
.
├── app.py              # Flask Application (The SUT - System Under Test)
├── config_data.py      # Test Data, Locators & Constants
├── conftest.py         # Shared Pytest Fixtures & Browser Setup
├── pages/              # Page Object Model (POM) Classes
│   ├── base_page.py    # Common UI actions & Base Page class
│   ├── actor_page.py   # Page Objects for Actor-related flows
│   └── film_page.py    # Page Objects for Film-related flows
├── tests/              # Test Suites
│   ├── api_tests/      # REST API validation tests
│   ├── db_tests/       # Database integrity & query tests
│   ├── ui_tests/       # Web UI functional tests
│   │   └── base_test.py # Base class for UI tests setup/teardown
│   └── e2e/            # Full End-to-End business scenarios
├── Jenkinsfile         # CI/CD Pipeline configuration
├── pytest.ini          # Pytest execution settings & markers
├── .env                # Environment variables (Secrets & Config)
└── requirements.txt    # Project dependencies

```

---

## 📝 Key Features

* **Synchronization:** Uses Selenium Explicit Waits (no `time.sleep` or unnecessary `refresh`).
* **Clean Code:** Decoupled test logic from UI locators using `config_data.py`.
* **Data Driven:** Parametrized tests for multiple data inputs.
* **Negative Testing:** Dedicated suites to verify error handling in API and UI.

---

## 🚀 CI/CD: Running Jenkins Locally

Jenkins is used to orchestrate the execution of the Sakila E2E testing suite. Follow these steps to run it on your local
machine.

### 1. Prerequisites

* **Java:** Version 17, 21, or 24 (See Startup for Java 24 fix).
* **Jenkins:** `jenkins.war` file downloaded from [Jenkins.io](https://www.jenkins.io/download/).

### 2. Startup Command

If you are using **Java 24** (or newer), you must use the `--enable-future-java` flag to bypass version restrictions:

```batch
java -jar jenkins.war --httpPort=8080 --enable-future-java

