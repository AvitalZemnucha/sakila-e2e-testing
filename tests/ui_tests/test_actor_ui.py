import pytest
from tests.base_test import BaseTest


class TestActorUI(BaseTest):

    def test_actor_list_page(self):
        """Verifies that the actor list is populated and visible."""
        self.actor_page.open()
        actor_list = self.actor_page.get_all_actors_elements()
        assert len(actor_list) > 0, "No actor list found"
        assert actor_list[0].is_displayed(), "Actor list is not displayed"

    @pytest.mark.parametrize("first_name, last_name", [
        ("NEW_Actor", "Last_Name"),
        ("John", "Doe"),
        ("QA_Test", "User"),
    ])
    def test_create_actor(self, first_name, last_name):
        """Tests the creation of new actors using multiple data sets."""
        self.actor_page.open()
        self.actor_page.add_actor(first_name, last_name)

        assert self.actor_page.is_text_present_in_table(first_name), \
            f"First name '{first_name}' not found anywhere in the table."

    @pytest.mark.parametrize("new_first_name, new_last_name", [
        ("AvitalUpdated", "ZemnuchaUpdated"),
        ("UpdatedJohn", "UpdatedDoe"),
        ("RenamedQA", "RenamedUser"),
    ])
    def test_update_actor(self, new_first_name, new_last_name):
        """Tests updating an existing actor and verifies the changes in the UI."""
        actor_id = 1
        self.actor_page.open()
        # Perform  update
        self.actor_page.update_actor(actor_id, new_first_name, new_last_name)
        updated_row_text = self.actor_page.get_actor_row_text(actor_id)
        assert new_first_name in updated_row_text, f"{new_first_name} not found in row!"
        assert new_last_name in updated_row_text, f"{new_last_name} not found in row!"

    def test_delete_actor(self):
        """Verifies that deleting an actor reduces the total count by one."""
        self.actor_page.open()
        # Capture initial state
        initial_count = len(self.actor_page.get_all_actors_elements())
        # Perform deletion
        self.actor_page.delete_last_actor()
        # Capture final state
        final_count = len(self.actor_page.get_all_actors_elements())
        assert final_count == initial_count - 1, "The actor was not deleted from the UI"
