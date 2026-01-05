import logging
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import Config

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def login_before_each(driver):
    """Auto-login before each test in this module."""
    login = LoginPage(driver)
    login.load()
    login.login(Config.STANDARD_USER, Config.PASSWORD)
    yield


class TestInventory:

    @pytest.mark.smoke
    @pytest.mark.inventory
    def test_inventory_page_loads_correctly(self, driver):
        """Inventory page title and product list visible after login."""
        inventory = InventoryPage(driver)
        assert inventory.is_loaded()
        assert inventory.get_page_title() == "Products"
        logger.info("✅ Inventory page loaded with 'Products' title")

    @pytest.mark.inventory
    def test_inventory_shows_six_products(self, driver):
        """Default inventory shows exactly 6 products."""
        inventory = InventoryPage(driver)
        count = inventory.get_product_count()
        assert count == 6, f"Expected 6 products, got {count}"
        logger.info(f"✅ Product count: {count}")

    @pytest.mark.inventory
    def test_add_single_product_updates_cart_badge(self, driver):
        """Adding one product increments the cart badge to 1."""
        inventory = InventoryPage(driver)
        inventory.add_product_to_cart("sauce-labs-backpack")

        count = inventory.get_cart_count()
        assert count == 1, f"Cart badge should be 1, got {count}"
        logger.info("✅ Cart badge updated to 1 after adding product")

    @pytest.mark.inventory
    def test_add_multiple_products_to_cart(self, driver):
        """Adding 3 products increments cart badge correctly."""
        inventory = InventoryPage(driver)
        inventory.add_product_to_cart("sauce-labs-backpack")
        inventory.add_product_to_cart("sauce-labs-bike-light")
        inventory.add_product_to_cart("sauce-labs-bolt-t-shirt")

        count = inventory.get_cart_count()
        assert count == 3, f"Expected 3 in cart, got {count}"
        logger.info(f"✅ Cart badge shows {count} after adding 3 products")

    @pytest.mark.inventory
    def test_sort_products_by_name_a_to_z(self, driver):
        """Products can be sorted A→Z; first item matches expected."""
        inventory = InventoryPage(driver)
        inventory.sort_products("az")
        names = inventory.get_all_product_names()
        assert names == sorted(names), f"Products not sorted A→Z: {names}"
        logger.info("✅ Products sorted A→Z correctly")

    @pytest.mark.inventory
    def test_sort_products_by_name_z_to_a(self, driver):
        """Products can be sorted Z→A."""
        inventory = InventoryPage(driver)
        inventory.sort_products("za")
        names = inventory.get_all_product_names()
        assert names == sorted(names, reverse=True)
        logger.info("✅ Products sorted Z→A correctly")
