"""Selenium driver helpers for morph lab automation."""

from __future__ import annotations

import os
from typing import Literal, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

DEFAULT_HUB_URL = os.getenv("HUB_URL", "http://127.0.0.1:4041")
SUPPORTED_BROWSERS = ("chrome", "firefox")


class UnsupportedBrowserError(RuntimeError):
    """Raised when attempting to start an unknown browser."""


def _build_chrome_options(headless: bool) -> ChromeOptions:
    options = ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if headless:
        options.add_argument("--headless=new")
    # Enable console logging so we can capture it later.
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    return options


def _build_firefox_options(headless: bool) -> FirefoxOptions:
    options = FirefoxOptions()
    options.set_preference("dom.disable_beforeunload", True)
    if headless:
        options.add_argument("-headless")
    return options


def create_driver(
    browser: Literal["chrome", "firefox"] = "chrome",
    hub_url: Optional[str] = None,
    headless: bool = True,
    implicit_wait: float = 5.0,
) -> webdriver.Remote:
    """Create a configured remote driver talking to the Selenium hub."""

    browser = browser.lower()
    if browser not in SUPPORTED_BROWSERS:
        raise UnsupportedBrowserError(f"Unsupported browser '{browser}'.")

    hub = hub_url or DEFAULT_HUB_URL

    if browser == "chrome":
        options = _build_chrome_options(headless)
    else:
        options = _build_firefox_options(headless)

    driver = webdriver.Remote(
        command_executor=hub,
        options=options,
    )
    driver.implicitly_wait(implicit_wait)
    driver.set_window_size(1400, 900)
    return driver
