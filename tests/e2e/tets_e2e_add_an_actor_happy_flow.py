import requests
from faker import Faker
from tests.base_test import BaseTest
from pages.actor_page import ActorPage
from config_data import ACTORS_API_URL


class TestActorHappyFlowE2E(BaseTest):
    actor_page: ActorPage

    def test_add_and_delete_actor_full_lifecycle(self, db_connection):
        """
        E2E Happy Flow — full actor lifecycle:
        1. CREATE  : POST new actor via API  → assert 201 + correct name returned.
        2. UI CHECK: open actor page         → assert new actor appears as last row.
        3. DELETE  : DELETE actor via API    → assert 204.
        4. DB CHECK: query by id             → assert row is gone.
        """
        fake = Faker()
        first_name = fake.first_name()
        last_name = fake.last_name()

        # ── Step 1: CREATE ────────────────────────────────────────────
        response = requests.post(ACTORS_API_URL, json={
            "first_name": first_name,
            "last_name": last_name,
            "last_update": "2006-02-15 04:34:33"
        })
        assert response.status_code == 201, (f"Expected 201 Created, got {response.status_code}: {response.json()}")
        actor_data = response.json()
        actor_id = actor_data["id"]

        assert actor_data["first_name"] == first_name, (
            f"First name mismatch. Expected '{first_name}', got '{actor_data['first_name']}'")

        # ── Step 2: UI CHECK ──────────────────────────────────────────
        self.actor_page.open()

        last_actor = self.actor_page.get_last_actor_row()
        assert last_actor is not None, "Actor table is empty — cannot verify."
        assert first_name in last_actor.text, (
            f"New actor '{first_name}' not found in last row. Got: '{last_actor.text}'")

        # ── Step 3: DELETE ────────────────────────────────────────────
        response = requests.delete(f"{ACTORS_API_URL}/{actor_id}")
        assert response.status_code == 204, (f"Expected 204 No Content on delete, got {response.status_code}")

        # ── Step 4: DB CHECK ──────────────────────────────────────────
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM actor WHERE actor_id = %s", (actor_id,))
        assert cursor.fetchone() is None, (f"Actor id {actor_id} still exists in the database after deletion.")
        cursor.close()
