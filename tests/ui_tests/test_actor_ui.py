import pytest
from pages.actor_page import ActorPage
from selenium.webdriver.common.by import By


def test_actor_list_page(actor_page):
    actor_page.open()
    actor_list = actor_page.get_all_actors_elements()
    assert len(actor_list) > 0, "No actor list found"
    assert actor_list[0].is_displayed(), "Actor list is not displayed"


@pytest.mark.parametrize("first_name, last_name", [
    ("NEW_Actor", "Last_Name"),
    ("John", "Doe"),
    ("QA_Test", "User"),
])
def test_create_actor(actor_page, first_name, last_name):
    actor_page.open()
    actor_page.add_actor(first_name, last_name)

    # אימות שהשחקן נוסף
    actors = actor_page.get_all_actors_elements()
    last_actor_text = actors[-1].text

    assert first_name in last_actor_text, f"First name {first_name} not found"
    assert last_name in last_actor_text, f"Last name {last_name} not found"


@pytest.mark.parametrize("new_first_name, new_last_name", [
    ("AvitalUpdated", "ZemnuchaUpdated"),
    ("UpdatedJohn", "UpdatedDoe"),
    ("RenamedQA", "RenamedUser"),
])
def test_update_actor(actor_page, new_first_name, new_last_name):
    actor_page.open()

    # העדכון עכשיו כולל המתנה פנימית בתוך ה-Page Object
    actor_page.update_actor(1, new_first_name, new_last_name)

    updated_row_text = actor_page.driver.find_element(By.ID, "actor-1").text

    assert new_first_name in updated_row_text
    assert new_last_name in updated_row_text
    assert new_last_name in updated_row_text


def test_delete_actor(actor_page):
    actor_page.open()
    # ספירת השחקנים לפני מחיקה
    initial_count = len(actor_page.get_all_actors_elements())
    # ביצוע מחיקה של האחרון
    actor_page.delete_last_actor()
    # אימות שהכמות קטנה ב-1
    final_count = len(actor_page.get_all_actors_elements())

    assert final_count == initial_count - 1, "The actor was not deleted from the UI"
