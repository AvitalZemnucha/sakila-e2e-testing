from pages.base_page import BasePage
from PIL import Image, ImageChops
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
        self.wait_for_element_visible(By.XPATH, ACTOR_LIST)

    # --- Edit Flow ---
    def open_edit_modal(self, actor_id):
        edit_xpath = f"//tr[@id='actor-{actor_id}']//button[contains(text(), 'Edit')]"
        self.click((By.XPATH, edit_xpath))

    def clear_edit_form(self):
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
        """Always re-fetches from DOM to avoid StaleElementReferenceException."""
        self.wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
        return self.driver.find_elements(By.XPATH, ACTOR_LIST)

    def test_create_actor(self, first_name, last_name):
        """Tests the creation of new actors using multiple data sets."""
        self.actor_page.open()
        self.actor_page.add_actor(first_name, last_name)

        assert self.actor_page.is_text_present_in_table(first_name), \
            f"First name '{first_name}' not found anywhere in the table."

    def is_text_present_in_table(self, text):
        """Re-fetches rows fresh to avoid StaleElementReferenceException after page update."""
        self.wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
        rows = self.driver.find_elements(By.XPATH, ACTOR_LIST)
        for row in rows:
            try:
                if text in row.text:
                    return True
            except Exception:
                # Row went stale mid-iteration — re-fetch and retry once
                rows = self.driver.find_elements(By.XPATH, ACTOR_LIST)
                if any(text in r.text for r in rows):
                    return True
        return False

    def delete_actor_by_name(self, first_name):
        """Scroll button into view and use JS click to bypass ElementClickInterceptedException."""
        self.wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
        rows = self.driver.find_elements(By.XPATH, ACTOR_LIST)
        for row in rows:
            try:
                if first_name in row.text:
                    delete_btn = row.find_element(By.XPATH, ".//button[contains(text(), 'Delete')]")
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_btn)
                    self.driver.execute_script("arguments[0].click();", delete_btn)
                    self.wait.until(EC.alert_is_present())
                    self.driver.switch_to.alert.accept()
                    break
            except Exception:
                continue

    def delete_last_actor(self) -> None:
        """Delete the last actor row in the table."""
        rows = self.get_all_actors_elements()
        if not rows:
            return
        delete_btn = rows[-1].find_element(By.XPATH, ".//button[contains(text(), 'Delete')]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_btn)
        self.driver.execute_script("arguments[0].click();", delete_btn)
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        self.wait.until(EC.staleness_of(rows[-1]))

    # --- Validation Helpers ---
    def get_field_validation_message(self, field_id):
        return self.get_validation_message((By.ID, field_id))

    def get_any_error_message_from_open_modal(self, first_name: str, last_name: str):
        """
        Called immediately after submit while modal is still visible.
        Checks the empty field for a validation message, or catches an alert.
        """
        field_id = EDIT_FIRST_NAME_ID if not first_name else EDIT_LAST_NAME_ID

        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            msg = alert.text
            alert.accept()
            return msg, "alert"
        except Exception:
            pass

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

    # --- Screenshot & Visual Regression ---
    def take_screenshot(self, name: str):
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
