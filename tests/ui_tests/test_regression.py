import pytest
from tests.base_test import BaseTest


class TestRegression(BaseTest):
    """
    Regression Test: Ensures adding an actor reflects in the UI
    both functionally and visually.
    """

    def test_actor_lifecycle_regression(self):
        first_n, last_n = "Visual", "Test_Actor"
        # Setup & Baseline
        self.actor_page.open()
        self.actor_page.take_screenshot("baseline.png")
        # Functional Action
        self.actor_page.add_actor(first_n, last_n)
        # Functional Verification
        assert self.actor_page.is_text_present_in_table(first_n), "New actor not found in table."
        # Visual Verification
        has_changed = self.actor_page.compare_screenshots("baseline.png", "current.png")
        assert has_changed, "Visual regression failed: Table did not change after adding actor."
        # Cleanup
        self.actor_page.delete_actor_by_name(first_n)
