from tests.base_test import BaseTest
import pytest
from selenium.webdriver.common.by import By
from pages.actor_page import ActorPage

from config_data import (
    FIRST_NAME_ID,
    LAST_NAME_ID,
    EDIT_FIRST_NAME_ID,
    EDIT_LAST_NAME_ID,
    UPDATE_BUTTON
)


class TestNegativeFlow(BaseTest):
    actor_page: ActorPage

    @pytest.mark.parametrize("first_name, last_name, missing_field_id", [
        ("", "Smith", FIRST_NAME_ID),
        ("John", "", LAST_NAME_ID),
        ("", "", FIRST_NAME_ID),
    ])
    def test_add_actor_negative_parametrized(self, first_name: str, last_name: str, missing_field_id: str):
        self.actor_page.open()
        self.actor_page.click_add_new_actor()
        self.actor_page.fill_new_actor_form(first_name=first_name, last_name=last_name)
        self.actor_page.submit_new_actor_form()

        validation_message = self.actor_page.get_field_validation_message(missing_field_id)
        assert validation_message == "Please fill out this field."

    def test_search_for_non_existing_actor(self):
        self.actor_page.open()
        search_term = "NICKNICK"
        is_found = self.actor_page.is_text_present_in_table(search_term)
        assert not is_found

    def test_edit_actor_empty_fields_validation(self):
        self.actor_page.open()
        self.actor_page.open_edit_modal(actor_id=1)
        self.actor_page.clear_edit_form()

        # Accessing driver via self.actor_page
        self.actor_page.driver.find_element(By.XPATH, UPDATE_BUTTON).click()

        validation_msg = self.actor_page.get_field_validation_message(EDIT_FIRST_NAME_ID)
        assert validation_msg == "Please fill out this field."

    @pytest.mark.parametrize("new_first, new_last, error_type, reason", [
        ("", "UpdatedLast", "validation", "Empty first name"),
        ("UpdatedFirst", "", "validation", "Empty last name"),
        ("", "", "validation", "Both fields empty"),
        ("A" * 101, "Last", "alert", "First name overflow"),
        ("First", "B" * 101, "alert", "Last name overflow"),
    ])
    def test_edit_actor_negative_parametrized(self, new_first, new_last, error_type, reason):
        self.actor_page.open()
        # update_actor_fields now returns (msg, type) while modal is still open
        actual_msg, actual_type = self.actor_page.update_actor_fields(actor_id=1, first_name=new_first,
                                                                      last_name=new_last)
        assert actual_type == error_type, (f"[{reason}] Expected '{error_type}', got '{actual_type}'")
        if error_type == "validation":
            assert "fill out this field" in actual_msg.lower(), (
                f"[{reason}] Expected validation message, got: '{actual_msg}'")
        else:
            assert "Error updating actor" in actual_msg, (f"[{reason}] Expected alert, got: '{actual_msg}'")
