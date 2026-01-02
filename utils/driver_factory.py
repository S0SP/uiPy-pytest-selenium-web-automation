import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config.settings import Config

logger = logging.getLogger(__name__)


class DriverFactory:
    """
    Creates and configures WebDriver instances.
    Supports Chrome and Firefox with headless mode.
    Selenium 4.6+ auto-manages driver binaries via Selenium Manager.
    """

    @staticmethod
    def get_driver(browser: str = None, headless: bool = None) -> webdriver.Remote:
        browser = (browser or Config.BROWSER).lower()
        headless = headless if headless is not None else Config.HEADLESS

        logger.info(f"🌐 Launching browser: {browser} | headless={headless}")

        if browser == "chrome":
            return DriverFactory._chrome_driver(headless)
        elif browser == "firefox":
            return DriverFactory._firefox_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: '{browser}'. Use 'chrome' or 'firefox'.")

    @staticmethod
    def _chrome_driver(headless: bool) -> webdriver.Chrome:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Selenium 4.6+ auto-downloads chromedriver via Selenium Manager
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        return driver

    @staticmethod
    def _firefox_driver(headless: bool) -> webdriver.Firefox:
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        # Selenium 4.6+ auto-downloads geckodriver via Selenium Manager
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        return driver
