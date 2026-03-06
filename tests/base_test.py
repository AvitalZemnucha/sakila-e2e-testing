import pytest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.actor_page import ActorPage
    from pages.film_page import FilmPage
    from selenium.webdriver.remote.webdriver import WebDriver


@pytest.mark.usefixtures("driver")
class BaseTest:
    driver: 'WebDriver'
    actor_page: 'ActorPage'
    film_page: 'FilmPage'

    @pytest.fixture(autouse=True)
    def setup_pages(self, driver: 'WebDriver'):
        from pages.actor_page import ActorPage
        from pages.film_page import FilmPage
        self.driver = driver
        self.actor_page = ActorPage(driver)
        self.film_page = FilmPage(driver)
        yield
