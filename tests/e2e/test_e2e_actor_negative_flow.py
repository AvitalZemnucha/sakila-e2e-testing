import pytest
import requests
from tests.base_test import BaseTest
from config_data import API_BASE_URL, INVALID_ACTOR_DATA


class TestNegativeFlowE2EActor(BaseTest):
    def test_add_actor_with_invalid_first_name(self):
        """
               E2E Negative Flow:
               1. API must reject an actor with empty first/last name (400).
               2. UI must confirm the invalid actor was never added to the table.
        """
        response = requests.post(f"{API_BASE_URL}actors", json=INVALID_ACTOR_DATA)
        assert response.status_code == 400, (f"Expected 400 Bad Request, got {response.status_code}"
                                             )
        assert "First name and last name are required" in response.json().get("error", ""), (
            f"Unexpected error message: {response.json()}"
        )
        self.actor_page.open()
        last_actor = self.actor_page.get_last_actor_row()
        assert last_actor is not None, "Actor table is empty — cannot verify."
        assert "Danielle" not in last_actor.text, (
            f"Invalid actor appeared in the table. Last row: '{last_actor.text}'"
        )
