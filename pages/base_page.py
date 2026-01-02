import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10


class BasePage:
    """
    Base class for all Page Objects.
    Encapsulates Selenium boilerplate — all pages inherit from here.
    """

    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # ── Navigation ─────────────────────────────────────────

    def open(self, url: str):
        logger.info(f"🌐 Navigating to: {url}")
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    # ── Wait helpers ────────────────────────────────────────

    def wait_for_element(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element not found after {timeout}s: {locator}")

    def wait_for_visible(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_url_contains(self, text: str, timeout: int = DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )

    def wait_for_text_in_element(self, locator: tuple, text: str, timeout: int = DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    # ── Interaction helpers ─────────────────────────────────

    def click(self, locator: tuple):
        element = self.wait_for_clickable(locator)
        logger.debug(f"🖱️  Clicking: {locator}")
        element.click()

    def type_text(self, locator: tuple, text: str):
        element = self.wait_for_visible(locator)
        element.clear()
        logger.debug(f"⌨️  Typing '{text}' into: {locator}")
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        element = self.wait_for_visible(locator)
        return element.text.strip()

    def is_displayed(self, locator: tuple) -> bool:
        try:
            element = self.wait_for_element(locator, timeout=5)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def get_elements(self, locator: tuple) -> list:
        self.wait_for_element(locator)
        return self.driver.find_elements(*locator)

    def get_element_count(self, locator: tuple) -> int:
        return len(self.get_elements(locator))
