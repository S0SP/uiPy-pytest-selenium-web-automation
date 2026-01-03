import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import Config

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page Object for the SauceDemo login page."""

    URL = Config.BASE_URL

    # ── Locators ─────────────────────────────────────────────
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # ── Actions ──────────────────────────────────────────────

    def load(self):
        self.open(self.URL)
        self.wait_for_visible(self.USERNAME_INPUT)
        logger.info("✅ Login page loaded")
        return self

    def enter_username(self, username: str):
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str):
        """Full login flow — chain of actions."""
        logger.info(f"🔑 Logging in as: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ── Assertions ───────────────────────────────────────────

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_displayed(self.ERROR_MESSAGE)

    def is_on_login_page(self) -> bool:
        """Check if we've returned to the login page after logout."""
        import time
        # Allow time for page redirect after logout
        for _ in range(10):
            url = self.get_current_url()
            if "inventory" not in url and "cart" not in url:
                break
            time.sleep(0.5)
        buttons = self.driver.find_elements(*self.LOGIN_BUTTON)
        return len(buttons) > 0 and buttons[0].is_displayed()
