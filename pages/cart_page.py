import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Page Object for the SauceDemo cart page."""

    # ── Locators ─────────────────────────────────────────────
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")

    # ── Actions ──────────────────────────────────────────────

    def is_loaded(self) -> bool:
        return "cart" in self.get_current_url()

    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def get_cart_items(self) -> list:
        elements = self.get_elements(self.ITEM_NAMES)
        return [el.text.strip() for el in elements]

    def get_cart_item_count(self) -> int:
        """Return number of items in cart. Returns 0 if cart is empty (no timeout)."""
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)

    def click_checkout(self):
        logger.info("💳 Proceeding to checkout")
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BTN)
