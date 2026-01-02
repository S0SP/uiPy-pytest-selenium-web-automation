import logging
import os
from datetime import datetime
from selenium import webdriver

logger = logging.getLogger(__name__)


def take_screenshot(driver: webdriver.Remote, test_name: str, screenshot_dir: str = "reports/screenshots") -> str:
    """Capture screenshot and save to disk. Returns the file path."""
    os.makedirs(screenshot_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize test name for filesystem
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in test_name)
    filename = f"{safe_name}_{timestamp}.png"
    filepath = os.path.join(screenshot_dir, filename)

    driver.save_screenshot(filepath)
    logger.info(f"📸 Screenshot saved: {filepath}")
    return filepath
