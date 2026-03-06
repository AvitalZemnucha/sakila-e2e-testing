from pages.base_page import BasePage
from PIL import Image, ImageChops
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config_data import (
    UI_BASE_URL, ACTOR_LIST, CREATE_NEW_ACTOR, NEW_ACTOR_SUBMIT,
    FIRST_NAME_ID, LAST_NAME_ID, EDIT_FIRST_NAME_ID,
    EDIT_LAST_NAME_ID, UPDATE_BUTTON
)


class ActorPage(BasePage):

    # --- Navigation ---
    def open(self):
        self.driver.get(UI_BASE_URL)
        return self

    # --- Creation & Regression Flow ---
    def click_add_new_actor(self):
        self.click((By.XPATH, CREATE_NEW_ACTOR))

    def fill_new_actor_form(self, first_name="", last_name=""):
        if first_name is not None:
            self.write((By.ID, FIRST_NAME_ID), first_name)
        if last_name is not None:
            self.write((By.ID, LAST_NAME_ID), last_name)

    def submit_new_actor_form(self):
        self.click((By.XPATH, NEW_ACTOR_SUBMIT))

    def add_actor(self, first_name: str, last_name: str) -> None:
        """Fill and submit the Add Actor form, then wait for the table to refresh."""
        self.click_add_new_actor()
        self.fill_new_actor_form(first_name, last_name)
        self.submit_new_actor_form()
        # Wait for table to refresh using the existing locator from config
        self.wait_for_element_visible(By.XPATH, ACTOR_LIST)

    # --- Edit Flow ---
    def open_edit_modal(self, actor_id):
        edit_xpath = f"//tr[@id='actor-{actor_id}']//button[contains(text(), 'Edit')]"
        self.click((By.XPATH, edit_xpath))

    def clear_edit_form(self):
        """NEW: Clears fields in the edit modal to fix unresolved reference."""
        self.driver.find_element(By.ID, EDIT_FIRST_NAME_ID).clear()
        self.driver.find_element(By.ID, EDIT_LAST_NAME_ID).clear()

    def update_actor(self, actor_id: int, first_name: str, last_name: str) -> None:
        self.open_edit_modal(actor_id)
        self.clear_edit_form()
        self.fill_edit_form(first_name, last_name)
        self.submit_edit_form()
        self.wait_for_element_visible(By.XPATH, ACTOR_LIST)

    def update_actor_fields(self, actor_id, first_name="", last_name=""):
        """Submit the edit form and return (message, type) immediately."""
        self.open_edit_modal(actor_id)
        self.clear_edit_form()
        self.fill_edit_form(first_name, last_name)
        self.submit_edit_form()
        # Read validation message NOW — modal is still open if validation failed
        return self.get_any_error_message_from_open_modal(first_name, last_name)

    def fill_edit_form(self, first_name="", last_name=""):
        if first_name is not None:
            self.write((By.ID, EDIT_FIRST_NAME_ID), first_name)
        if last_name is not None:
            self.write((By.ID, EDIT_LAST_NAME_ID), last_name)

    def submit_edit_form(self):
        self.click((By.XPATH, UPDATE_BUTTON))

    # --- Table Actions & Verification ---
    def get_all_actors_elements(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
        return self.driver.find_elements(By.XPATH, ACTOR_LIST)

    def get_last_actor_row(self):
        """NEW: Returns the last row element in the actor table."""
        rows = self.get_all_actors_elements()
        return rows[-1] if rows else None

    def is_text_present_in_table(self, text):
        """NEW: Verifies text presence to fix unresolved reference."""
        rows = self.get_all_actors_elements()
        return any(text in row.text for row in rows)

    def delete_actor_by_name(self, first_name):
        """NEW: Cleanup helper for regression tests."""
        rows = self.get_all_actors_elements()
        for row in rows:
            if first_name in row.text:
                delete_btn = row.find_element(By.XPATH, ".//button[contains(text(), 'Delete')]")
                delete_btn.click()
                self.wait.until(EC.alert_is_present())
                self.driver.switch_to.alert.accept()
                break

    def delete_last_actor(self) -> None:
        """Delete the last actor row in the table."""
        rows = self.get_all_actors_elements()
        if not rows:
            return
        delete_btn = rows[-1].find_element(By.XPATH, ".//button[contains(text(), 'Delete')]")
        delete_btn.click()
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        # Wait for the row to disappear before returning
        self.wait.until(EC.staleness_of(rows[-1]))

    # --- Validation Helpers ---
    def get_field_validation_message(self, field_id):
        """FIXED: Renamed to match TestNegativeFlow call."""
        return self.get_validation_message((By.ID, field_id))

    def get_any_error_message_from_open_modal(self, first_name: str, last_name: str):
        """
        Called immediately after submit while modal is still visible.
        Checks the empty field for a validation message, or catches an alert.
        """
        # Determine which field to check — the one that was left empty
        field_id = EDIT_FIRST_NAME_ID if not first_name else EDIT_LAST_NAME_ID

        # Check for JS alert first (overflow case) with short timeout
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            msg = alert.text
            alert.accept()
            return msg, "alert"
        except Exception:
            pass

        # Modal still open — read HTML5 validation message directly from the field
        try:
            field = self.driver.find_element(By.ID, field_id)
            msg = self.driver.execute_script("return arguments[0].validationMessage;", field)
            return msg or "", "validation"
        except Exception:
            return "", "unknown"

    def get_actor_row_text(self, actor_id: int) -> str:
        """Return the full text of the row matching actor_id, waiting for it to be visible."""
        try:
            row = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//tr[@id='actor-{actor_id}']"))
            )
            return row.text
        except Exception:
            return ""

    def take_screenshot(self, name: str):
        """Saves a screenshot to the current directory."""
        self.driver.save_screenshot(name)

    def compare_screenshots(self, baseline_path: str, current_path: str):
        """
        Compares two screenshots.
        Saves a diff file and returns True if a difference is detected.
        """
        self.take_screenshot(current_path)

        img1 = Image.open(baseline_path).convert("RGB")
        img2 = Image.open(current_path).convert("RGB")

        diff = ImageChops.difference(img1, img2)
        bbox = diff.getbbox()

        if bbox:
            diff.save("visual_diff_result.png")
            return True
        return False
