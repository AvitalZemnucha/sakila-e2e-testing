# pages/film_page.py
from pages.base_page import BasePage
from config_data import RESULT_TEXT, TOP_RATED_LINK
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class FilmPage(BasePage):
    # This matches the result info locator in your UI
    _TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    _H1 = (By.TAG_NAME, "h1")

    def open_top_rated(self):
        self.driver.get(TOP_RATED_LINK)

    def wait_for_results_to_load(self) -> bool:
        """Wait for table rows to appear — this page has no DataTables info bar."""
        try:
            self.wait.until(EC.presence_of_element_located(self._TABLE_ROWS))
            return True
        except Exception:
            return False

    def is_top_rated_header_correct(self) -> bool:
        return self.wait_for_text_in_element(By.TAG_NAME, "h1", "Top Rated Films")

    def is_text_present_in_table(self, text: str) -> bool:
        try:
            table = self.driver.find_element(By.TAG_NAME, "table")
            return text in table.text
        except Exception:
            return False

    # pages/film_page.py  — add these three methods
    from config_data import TOP_RATED_LINK

    _LAST_PAGE = 23  # last page of top rated films

    def open_last_page(self):
        """Navigate directly to the last pagination page for boundary verification."""
        self.driver.get(f"{TOP_RATED_LINK}?page={self._LAST_PAGE}")
        self.wait_for_results_to_load()

    def get_table_row_count(self) -> int:
        """Return the number of data rows currently visible in the table."""
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table td")
        return len(rows)

    def refresh(self):
        """Reload the current page and wait for the table to re-render."""
        self.driver.refresh()
        self.wait_for_results_to_load()
