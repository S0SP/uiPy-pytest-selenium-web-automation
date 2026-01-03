import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import Config

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    """Page Object for the SauceDemo products/inventory page."""

    URL = f"{Config.BASE_URL}/inventory.html"

    # ── Locators ─────────────────────────────────────────────
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def _add_to_cart_btn(self, product_name: str) -> tuple:
        """Dynamically build locator for a specific product's Add to Cart button."""
        data_test_id = f"add-to-cart-{product_name.lower().replace(' ', '-')}"
        return (By.CSS_SELECTOR, f"[data-test='{data_test_id}']")

    def _remove_from_cart_btn(self, product_name: str) -> tuple:
        data_test_id = f"remove-{product_name.lower().replace(' ', '-')}"
        return (By.CSS_SELECTOR, f"[data-test='{data_test_id}']")

    # ── Actions ──────────────────────────────────────────────

    def is_loaded(self) -> bool:
        return self.is_displayed(self.PAGE_TITLE) and "inventory" in self.get_current_url()

    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def get_all_product_names(self) -> list:
        elements = self.get_elements(self.ITEM_NAMES)
        return [el.text.strip() for el in elements]

    def get_product_count(self) -> int:
        return self.get_element_count(self.INVENTORY_ITEMS)

    def add_product_to_cart(self, product_name: str):
        """Add a product to cart by its exact display name."""
        logger.info(f"🛒 Adding to cart: {product_name}")
        self.click(self._add_to_cart_btn(product_name))

    def remove_product_from_cart(self, product_name: str):
        logger.info(f"❌ Removing from cart: {product_name}")
        self.click(self._remove_from_cart_btn(product_name))

    def get_cart_count(self) -> int:
        if not self.is_displayed(self.CART_BADGE):
            return 0
        badge_text = self.get_text(self.CART_BADGE)
        return int(badge_text)

    def go_to_cart(self):
        logger.info("🛒 Navigating to cart")
        self.click(self.CART_ICON)

    def sort_products(self, option_value: str):
        """Sort products by value (az, za, lohi, hilo)."""
        from selenium.webdriver.support.ui import Select
        dropdown = self.wait_for_visible(self.SORT_DROPDOWN)
        Select(dropdown).select_by_value(option_value)
        logger.info(f"🔀 Sorted products by: {option_value}")

    def logout(self):
        """Open sidebar menu and click logout."""
        import time
        self.click(self.BURGER_MENU)
        time.sleep(1)  # Sidebar CSS animation
        # Direct JS click — sidebar animation unreliable in headless Chrome
        el = self.driver.find_element(*self.LOGOUT_LINK)
        self.driver.execute_script("arguments[0].click();", el)
        time.sleep(1)  # Wait for redirect
        logger.info("🚪 Logged out successfully")
