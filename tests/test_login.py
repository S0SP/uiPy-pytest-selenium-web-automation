import logging
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import Config

logger = logging.getLogger(__name__)


class TestLogin:

    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login_redirects_to_inventory(self, driver):
        """Standard user can login successfully and lands on inventory page."""
        login = LoginPage(driver)
        inventory = InventoryPage(driver)

        login.load()
        login.login(Config.STANDARD_USER, Config.PASSWORD)

        assert inventory.is_loaded(), "Expected to land on inventory page after login"
        assert "Products" in inventory.get_page_title()
        logger.info("✅ Valid login: redirected to inventory page")

    @pytest.mark.login
    def test_invalid_password_shows_error(self, driver):
        """Wrong password shows error message."""
        login = LoginPage(driver)
        login.load()
        login.login(Config.STANDARD_USER, "wrong_password")

        assert login.is_error_displayed(), "Error message should appear for bad credentials"
        error = login.get_error_message()
        assert "Username and password do not match" in error
        logger.info(f"✅ Error shown for bad password: {error}")

    @pytest.mark.login
    def test_locked_user_shows_error(self, driver):
        """Locked-out user sees an appropriate error message."""
        login = LoginPage(driver)
        login.load()
        login.login(Config.LOCKED_USER, Config.PASSWORD)

        assert login.is_error_displayed()
        error = login.get_error_message()
        assert "locked out" in error.lower()
        logger.info(f"✅ Locked user error: {error}")

    @pytest.mark.login
    def test_empty_username_shows_error(self, driver):
        """Submitting with no username shows validation error."""
        login = LoginPage(driver)
        login.load()
        login.click_login()

        assert login.is_error_displayed()
        error = login.get_error_message()
        assert "Username is required" in error
        logger.info(f"✅ Empty username error: {error}")

    @pytest.mark.login
    def test_empty_password_shows_error(self, driver):
        """Submitting with no password shows validation error."""
        login = LoginPage(driver)
        login.load()
        login.enter_username(Config.STANDARD_USER)
        login.click_login()

        assert login.is_error_displayed()
        error = login.get_error_message()
        assert "Password is required" in error

    @pytest.mark.login
    def test_logout_returns_to_login(self, driver):
        """User can logout and is returned to login page."""
        login = LoginPage(driver)
        inventory = InventoryPage(driver)

        login.load()
        login.login(Config.STANDARD_USER, Config.PASSWORD)
        assert inventory.is_loaded()

        inventory.logout()
        # Wait for redirect from inventory page to complete
        import time
        time.sleep(2)
        assert login.is_on_login_page(), "Expected to return to login page after logout"
        logger.info("✅ Logout returns to login page")
