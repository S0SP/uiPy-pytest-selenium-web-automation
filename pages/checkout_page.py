import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    """Page Object for SauceDemo checkout step one and two pages."""

    # ── Locators: Step One ────────────────────────────────────
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # ── Locators: Step Two ────────────────────────────────────
    FINISH_BUTTON = (By.ID, "finish")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    # ── Locators: Confirmation ────────────────────────────────
    CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")

    # ── Actions ──────────────────────────────────────────────

    def fill_customer_info(self, first_name: str, last_name: str, postal: str):
        logger.info(f"📋 Filling info: {first_name} {last_name}, {postal}")
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal)

    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)

    def get_order_total(self) -> str:
        return self.get_text(self.SUMMARY_TOTAL)

    def click_finish(self):
        logger.info("✅ Clicking Finish")
        self.click(self.FINISH_BUTTON)

    def get_confirmation_message(self) -> str:
        return self.get_text(self.CONFIRMATION_HEADER)

    def is_order_confirmed(self) -> bool:
        return "Thank you" in self.get_confirmation_message()

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
