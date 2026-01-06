import logging
import os
import pytest
from selenium import webdriver
from utils.driver_factory import DriverFactory
from utils.logger import setup_logger
from utils.screenshot import take_screenshot
from config.settings import Config

setup_logger()
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────
# CLI options for browser / headless control
# ──────────────────────────────────────────

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=Config.BROWSER,
                     help="Browser to run tests: chrome or firefox")
    parser.addoption("--headless", action="store", default=str(Config.HEADLESS),
                     help="Run headless: true or false")


# ──────────────────────────────────────────
# Driver fixture — function scope (fresh per test)
# ──────────────────────────────────────────

@pytest.fixture(scope="function")
def driver(request) -> webdriver.Remote:
    browser = request.config.getoption("--browser")
    headless_flag = request.config.getoption("--headless").lower() == "true"

    logger.info(f"🚀 Starting {browser} driver | headless={headless_flag}")
    drv = DriverFactory.get_driver(browser=browser, headless=headless_flag)
    drv.maximize_window()

    yield drv

    drv.quit()
    logger.info("🛑 Browser closed")


# ──────────────────────────────────────────
# Auto-screenshot on test failure
# ──────────────────────────────────────────

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = take_screenshot(
                driver,
                test_name=item.name,
                screenshot_dir=Config.SCREENSHOT_DIR
            )
            logger.error(f"❌ Test FAILED: {item.nodeid}")
            logger.error(f"📸 Screenshot: {screenshot_path}")

            # Embed screenshot in HTML report
            if hasattr(report, "extras"):
                from pytest_html import extras
                report.extras = getattr(report, "extras", [])
                report.extras.append(extras.image(screenshot_path))


# ──────────────────────────────────────────
# Setup: ensure report dirs exist
# ──────────────────────────────────────────

def pytest_configure(config):
    os.makedirs("reports", exist_ok=True)
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
