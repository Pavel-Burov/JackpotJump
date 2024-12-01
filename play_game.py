# remote-scripts/play_game.py

import time
from playwright.sync_api import Playwright, sync_playwright
import sys

# Configuration settings
TEST_ACCOUNTS = 2  # Number of accounts to test (local test)
START_DELAY = 45  # Delay for the first account to wait before others start

canvas_coordinates = [
    (580, 600),
    (580, 535),
    (580, 465),
    (580, 400),
    (580, 330),
    (580, 260),
]


def start_game(page, account_id, delay):
    """
    Simulate clicking the start button for a specific account.
    """
    if account_id == 0:
        print(
            f"Account {account_id} clicking the start button after {delay} seconds...")
        page.locator("#GameCanvas").click(position={"x": 669, "y": 642})
        time.sleep(0.5)
        page.locator("#GameCanvas").click(position={"x": 757, "y": 520})
        time.sleep(0.5)
        page.locator("#GameCanvas").click(position={"x": 635, "y": 421})
        time.sleep(0.5)
        page.locator("#GameCanvas").click(position={"x": 635, "y": 421})
        print(f"Account {account_id} clicked the start button.")
        time.sleep(delay)
    else:
        print(f"Account {account_id} waiting for {delay} seconds...")
        time.sleep(delay)
        page.locator("#GameCanvas").click(position={"x": 669, "y": 642})
        time.sleep(0.5)
        page.locator("#GameCanvas").click(position={"x": 757, "y": 520})
        time.sleep(0.5)
        page.locator("#GameCanvas").click(position={"x": 635, "y": 421})
        time.sleep(0.5)
        page.locator("#GameCanvas").click(position={"x": 635, "y": 421})
        print(f"Account {account_id} clicked the start button.")


def open_game_and_play(account_id: int, delay: int = 0):
    """
    Opens the game for the specified account and simulates gameplay actions.
    """
    try:
        with sync_playwright() as p:
            # Launch the browser (Non-headless mode for testing)
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Navigate to the game page
            page.goto(
                "https://cdn.kingdomhall729.com/qat/jackpot-jump/2024-11-22-13-44-55/index.html?currency=THB")

            # Wait for the #GameCanvas element to be present and visible
            wait_for_canvas_clickable(page)
            print(f"Canvas element found for account {account_id}")
            time.sleep(20)

            # START GAME
            start_game(page, account_id, delay)

            # Game logic
            time.sleep(2)
            for x_offset, y_offset in canvas_coordinates:
                page.locator("#GameCanvas").click(
                    position={"x": x_offset, "y": y_offset})
                print(
                    f"Account {account_id} clicked at ({x_offset}, {y_offset})")
                time.sleep(0.5)

            time.sleep(50)
            context.close()
            browser.close()

    except Exception as e:
        print(f"Error with account {account_id}: {e}")


def wait_for_canvas_clickable(page):
    """
    Waits for the #GameCanvas element to be visible and clickable.
    """
    retries = 0
    max_retries = 10
    while retries < max_retries:
        try:
            page.locator("#GameCanvas").wait_for(state="visible", timeout=3000)
            page.locator("#GameCanvas").click(position={"x": 644, "y": 640})
            print("Canvas is visible and clickable.")
            break
        except Exception as e:
            retries += 1
            time.sleep(retries)
    else:
        raise Exception("Max retries reached. Canvas is not clickable.")


if __name__ == "__main__":
    account_id = int(sys.argv[1])  # Account ID passed as an argument
    delay = int(sys.argv[2])  # Delay passed as an argument
    open_game_and_play(account_id, delay)
