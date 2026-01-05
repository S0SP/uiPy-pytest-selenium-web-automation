import logging
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.settings import Config

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def login_before_each(driver):
    """Auto-login before each test in this module."""
    login = LoginPage(driver)
    login.load()
    login.login(Config.STANDARD_USER, Config.PASSWORD)
    yield


class TestCartAndCheckout:

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_added_product_appears_in_cart(self, driver):
        """Product added from inventory appears in cart with correct name."""
        inventory = InventoryPage(driver)
        inventory.add_product_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        cart = CartPage(driver)
        assert cart.is_loaded(), "Cart page did not load"
        items = cart.get_cart_items()
        assert "Sauce Labs Backpack" in items, f"Expected product in cart, got: {items}"
        logger.info(f"✅ Cart contains: {items}")

    @pytest.mark.cart
    def test_cart_item_count_matches(self, driver):
        """Cart page shows correct number of items."""
        inventory = InventoryPage(driver)
        inventory.add_product_to_cart("sauce-labs-backpack")
        inventory.add_product_to_cart("sauce-labs-bike-light")
        inventory.go_to_cart()

        cart = CartPage(driver)
        assert cart.get_cart_item_count() == 2
        logger.info("✅ Cart item count is 2")

    @pytest.mark.cart
    def test_empty_cart_has_no_items(self, driver):
        """Cart is empty when no products added."""
        inventory = InventoryPage(driver)
        inventory.go_to_cart()

        cart = CartPage(driver)
        assert cart.get_cart_item_count() == 0
        logger.info("✅ Cart is empty as expected")

    @pytest.mark.cart
    def test_full_checkout_flow_completes_successfully(self, driver):
        """
        End-to-end flow:
        Login → Add product → Cart → Checkout info → Confirm → Order complete
        """
        # Step 1: Add product to cart
        inventory = InventoryPage(driver)
        inventory.add_product_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        # Step 2: Proceed to checkout
        cart = CartPage(driver)
        assert cart.is_loaded()
        cart.click_checkout()

        # Step 3: Fill customer info
        checkout = CheckoutPage(driver)
        checkout.fill_customer_info("John", "Doe", "400001")
        checkout.click_continue()

        # Step 4: Verify total and finish
        total = checkout.get_order_total()
        assert "$" in total, f"Expected price total, got: {total}"
        logger.info(f"💰 Order total: {total}")
        checkout.click_finish()

        # Step 5: Confirm order complete
        assert checkout.is_order_confirmed(), "Order confirmation message not found"
        logger.info("✅ End-to-end checkout flow completed successfully")

    @pytest.mark.cart
    def test_checkout_requires_customer_info(self, driver):
        """Checkout step one shows error when info fields are empty."""
        inventory = InventoryPage(driver)
        inventory.add_product_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        cart = CartPage(driver)
        cart.click_checkout()

        checkout = CheckoutPage(driver)
        checkout.click_continue()

        error = checkout.get_error_message()
        assert "First Name is required" in error
        logger.info(f"✅ Empty checkout form error: {error}")

    @pytest.mark.cart
    @pytest.mark.parametrize("product_id,expected_name", [
        ("sauce-labs-backpack", "Sauce Labs Backpack"),
        ("sauce-labs-bike-light", "Sauce Labs Bike Light"),
        ("sauce-labs-bolt-t-shirt", "Sauce Labs Bolt T-Shirt"),
    ])
    def test_each_product_can_be_added_to_cart(self, driver, product_id, expected_name):
        """Parametrized: each product can be added and appears in cart."""
        inventory = InventoryPage(driver)
        inventory.add_product_to_cart(product_id)
        inventory.go_to_cart()

        cart = CartPage(driver)
        items = cart.get_cart_items()
        assert expected_name in items, f"'{expected_name}' not in cart: {items}"
        logger.info(f"✅ {expected_name} found in cart")
