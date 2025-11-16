"""End-to-end automation runner for FloAng Morph Lab."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List

import requests
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .driver_adapter import create_driver


def wait_for_server(url: str, timeout: float = 30.0, interval: float = 1.0) -> None:
    """Poll the dev server until it responds with 200 OK."""

    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        try:
            response = requests.get(url, timeout=5)
            if response.ok:
                return
        except requests.RequestException as exc:  # pragma: no cover - network
            last_error = exc
        time.sleep(interval)

    raise RuntimeError(f"Server {url} did not become ready: {last_error}")


def capture_console_logs(driver, run_id: str) -> List[Dict[str, Any]]:
    logs = []
    try:
        for entry in driver.get_log("browser"):
            logs.append(
                {
                    "runId": run_id,
                    "level": entry.get("level"),
                    "message": entry.get("message"),
                    "timestamp": entry.get("timestamp"),
                }
            )
    except WebDriverException as exc:
        logs.append(
            {
                "runId": run_id,
                "level": "ERROR",
                "message": f"Failed to fetch console logs: {exc}",
                "timestamp": time.time(),
            }
        )
    return logs


def persist_logs(logs: List[Dict[str, Any]], output_dir: str, run_id: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{run_id}.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(logs, handle, indent=2)
    return path


def forward_logs(logs: List[Dict[str, Any]], endpoint: str) -> None:
    response = requests.post(endpoint, json={"logs": logs}, timeout=10)
    response.raise_for_status()


def run_morph_sequence(driver, base_url: str, timeout: float = 120.0) -> None:
    driver.get(base_url)

    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.NULL)

    start_button = driver.find_element(By.CSS_SELECTOR, "button[onclick='startMorph()']")
    start_button.click()

    deadline = time.time() + timeout
    while time.time() < deadline:
        console_entries = driver.get_log("browser")
        if any("Morph complete" in entry.get("message", "") for entry in console_entries):
            return
        time.sleep(1)

    raise TimeoutError("Morph did not complete within timeout window")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Morph Lab automation")
    parser.add_argument("--server-url", default="http://localhost:8000/morph-lab.html")
    parser.add_argument("--run-id", default=str(int(time.time())))
    parser.add_argument("--browser", choices=("chrome", "firefox"), default="chrome")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--log-endpoint")
    parser.add_argument("--log-dir", default=".logs/morphlab")
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = parse_args(argv or sys.argv[1:])

    wait_for_server(args.server_url)

    driver = create_driver(browser=args.browser, headless=args.headless)
    try:
        run_morph_sequence(driver, args.server_url)
        logs = capture_console_logs(driver, args.run_id)

        if args.log_endpoint:
            forward_logs(logs, args.log_endpoint)
            print(f"Uploaded {len(logs)} console logs to {args.log_endpoint}")
        else:
            path = persist_logs(logs, args.log_dir, args.run_id)
            print(f"Saved console logs to {path}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
