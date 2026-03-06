# pages/base_page.py
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """
    Root page object. Centralising wait helpers here eliminates
    "Unresolved Reference" warnings in ActorPage and FilmPage.
    """
    driver: WebDriver  # class-level hint for subclass resolution

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # FIX: tuple[str, str] silences "Expected tuple[str, str], got tuple instead"
    def click(self, locator: tuple[str, str]):
        """Standardised click that waits for the element to be ready."""
        return self.wait.until(EC.element_to_be_clickable(locator)).click()

    # FIX: same explicit parameterised tuple hint on write()
    def write(self, locator: tuple[str, str], text: str):
        """Clears and fills a field once visible."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def wait_for_text_in_element(self, locator_type: str, locator_value: str, text: str) -> bool:
        """Wait until *text* appears inside the element."""
        try:
            self.wait.until(
                EC.text_to_be_present_in_element((locator_type, locator_value), text)
            )
            return True
        except Exception:
            return False

    def get_field_validation_message(self, field_id: str) -> str:
        """Helper specifically for IDs to match your TestNegativeFlow calls."""
        return self.get_validation_message((By.ID, field_id))

    def get_validation_message(self, locator: tuple[str, str]) -> str:
        """
        The actual engine: Finds the element and runs JavaScript
        to get the 'Please fill out this field' message.
        """
        element = self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.execute_script("return arguments[0].validationMessage;", element)

    def is_text_present_in_table(self, text: str) -> bool:
        """Return True if *text* appears anywhere in the page's first <table>."""
        try:
            table = self.driver.find_element(By.TAG_NAME, "table")
            return text in table.text
        except Exception:
            return False

    def wait_for_element_visible(self, locator_type: str, locator_value: str):
        """Return element once visible, or None on timeout."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located((locator_type, locator_value))
            )
        except Exception:
            return None
