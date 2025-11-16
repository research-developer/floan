"""Page object for morph-lab.html interactions."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from .base_page import BasePage


class MorphLabPage(BasePage):
    PATH = "morph-lab.html"

    START_BUTTON = (By.CSS_SELECTOR, "button[onclick='startMorph()']")
    RESET_BUTTON = (By.CSS_SELECTOR, "button[onclick='resetState()']")
    DEBUG_TOGGLE = (By.CSS_SELECTOR, "button[onclick='toggleDebugMode()']")
    PROGRESS_METRIC = (By.ID, "progress-metric")
    SIDES_VALUE = (By.ID, "sides-value")

    def visit(self) -> None:
        self.open(self.PATH)
        self.wait_for_visible(self.START_BUTTON)

    def start_morph(self) -> None:
        self.click(self.START_BUTTON)

    def reset(self) -> None:
        self.click(self.RESET_BUTTON)

    def toggle_debug_ui(self) -> None:
        self.click(self.DEBUG_TOGGLE)

    def get_progress_text(self) -> str:
        return self.find(self.PROGRESS_METRIC).text

    def get_sides_value(self) -> int:
        text = self.find(self.SIDES_VALUE).text
        return int(text.strip()) if text else 0
