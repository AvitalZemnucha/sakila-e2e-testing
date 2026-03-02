# Sakila E2E Test Automation Project

This project provides a full-stack end-to-end testing solution for the Sakila Sample Database application. It includes a Python Flask web application and a comprehensive test suite covering **UI (Selenium)**, **API (Requests)**, and **Database (SQLAlchemy)** testing.

## 🚀 Project Architecture

The project follows the **Page Object Model (POM)** pattern for UI tests and uses a centralized `conftest.py` for shared fixtures.

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
├── app.py              # Flask Application
├── config_data.py      # Test Data & Locators (Constants)
├── conftest.py         # Shared Pytest Fixtures
├── pages/              # Page Object Model (POM) Classes
│   └── actor_page.py
├── tests/              # Test Packages
│   ├── api_tests/
│   ├── db_tests/
│   ├── ui_tests/
│   └── e2e/
└── pytest.ini          # Pytest Configuration

```

---

## 📝 Key Features

* **Synchronization:** Uses Selenium Explicit Waits (no `time.sleep` or unnecessary `refresh`).
* **Clean Code:** Decoupled test logic from UI locators using `config_data.py`.
* **Data Driven:** Parametrized tests for multiple data inputs.
* **Negative Testing:** Dedicated suites to verify error handling in API and UI.

---

