from __future__ import annotations
import logging

from reportportal_client import step

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class HomePage:

    @step
    def get_title(self) -> str:
        return "Home Page"

class LoginPage:

    @step
    def click_on_login_btn(self) -> HomePage:
        logger.info("Clicking on log in btb")
        return HomePage()

    @step
    def fill_username_tb(self, username):
        logger.info(f"Fill {username} to username tb")

    @step
    def fill_password_tb(self, password):
        logger.info(f"Fill {password} to password tb")


def test_report_manager_with_fixture(rp_logger):
    rp_logger.debug("Some debug message")
    rp_logger.info("Some info message")


def test_nested_stpes():
    logger.info("About to start test")
    login_page = LoginPage()
    login_page.fill_username_tb(username="Itai")
    login_page.fill_password_tb(password="something")
    home_page = login_page.click_on_login_btn()
    title = home_page.get_title()
    assert title == "Home Page"
        # .fill_password_tb(password="secret")
        # .click_on_login_btn()
    logger.info("Ending test")


