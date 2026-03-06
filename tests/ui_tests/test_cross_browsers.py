from tests.base_test import BaseTest


class TestAcrossBrowsers(BaseTest):
    def test_cross_browsers(self):
        """
        By inheriting from BaseTest, we access the page object via self.
        """
        # The IDE will now correctly resolve self.actor_page.driver.name
        print(f"Running test on browser: {self.actor_page.driver.name}")

        self.actor_page.open()
        actor_list = self.actor_page.get_all_actors_elements()

        assert len(actor_list) > 0, "Actor list should not be empty"
