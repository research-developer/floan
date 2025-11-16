"""Shared utilities for FloAng Selenium page objects."""

from __future__ import annotations

from typing import Callable, Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Simple base class that wraps a Selenium driver with wait helpers."""

    def __init__(self, driver: WebDriver, base_url: Optional[str] = None, timeout: int = 20) -> None:
        self._driver = driver
        self.base_url = base_url.rstrip("/") if base_url else None
        self.wait = WebDriverWait(driver, timeout)

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------
    def open(self, path: str) -> None:
        """Navigate to `base_url/path` (or absolute path if base_url unset)."""

        if self.base_url:
            url = f"{self.base_url}/{path.lstrip('/')}"
        else:
            url = path
        self._driver.get(url)

    # ------------------------------------------------------------------
    # Wait helpers
    # ------------------------------------------------------------------
    def wait_for_visible(self, locator) -> None:
        self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_condition(self, predicate: Callable[[WebDriver], bool], message: str = "") -> None:
        self.wait.until(predicate, message)

    # ------------------------------------------------------------------
    # Convenience wrappers
    # ------------------------------------------------------------------
    def find(self, locator):
        return self._driver.find_element(*locator)

    def click(self, locator) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def set_checkbox(self, locator, checked: bool) -> None:
        element = self.find(locator)
        if element.is_selected() != checked:
            element.click()

    @property
    def driver(self) -> WebDriver:
        return self._driver
