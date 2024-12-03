import time
from playwright.sync_api import Playwright, sync_playwright
from concurrent.futures import ThreadPoolExecutor
import threading
import sys

# Configuration settings
TEST_ACCOUNTS = 2  # Number of accounts to test (local test)
START_DELAY = 45  # Delay for all accounts to wait before starting

# Coordinates for the GameCanvas clicks (replace with your actual values)
canvas_coordinates = [
    (580, 600),
    (580, 535),
    (580, 465),
    (580, 400),
    (580, 330),
    (580, 260),
]

# Shared event to sync threads after splash screen disappears
splash_screen_event = threading.Event()

# Shared event to signal that the game is ready to start
start_event = threading.Event()


def wait_for_splash_screen_to_disappear(page):
    retries = 0
    max_retries = 30
    while retries < max_retries:
        splash_div = page.locator("#splash")
        if splash_div.is_visible() and splash_div.evaluate("el => el.style.display === 'block'"):
            print(
                f"{retries} — Splash screen visible. Waiting for it to disappear...")
            time.sleep(1)
            retries += 1
        else:
            print("Splash screen has disappeared.")
            splash_screen_event.set()  # Notify the other threads
            break
    else:
        print("Splash screen didn't disappear after retries.")


def prompt_for_start():
    """
    Prompts the user to start the game.
    """
    start_input = input("Are we starting? (y/n): ").strip().lower()
    if start_input == 'y':
        start_event.set()  # Signal to start the game
    elif start_input == 'n':
        print("Game not started. Exiting...")
        sys.exit(0)
    else:
        print("Invalid input. Please enter 'y' to start or 'n' to exit.")
        prompt_for_start()  # Retry if invalid input


def start_game(page, account_id, delay):
    print(
        f"Account {account_id} clicking the start button after {delay} seconds...")
    page.locator("#GameCanvas").click(position={"x": 669, "y": 642})
    time.sleep(0.5)
    page.locator("#GameCanvas").click(position={"x": 757, "y": 520})
    time.sleep(0.5)
    page.locator("#GameCanvas").click(position={"x": 757, "y": 520})
    time.sleep(0.5)
    page.locator("#GameCanvas").click(position={"x": 635, "y": 421})
    time.sleep(0.5)
    page.locator("#GameCanvas").click(position={"x": 635, "y": 421})
    print(f"Account {account_id} clicked the start button.")
    time.sleep(delay)


def open_game(account_id: int, delay: int = 0):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            page.goto(
                "https://cdn.kingdomhall729.com/qat/jackpot-jump/2024-11-22-13-44-55/index.html?currency=THB")

            wait_for_splash_screen_to_disappear(page)
            splash_screen_event.wait()  # Ensure the splash screen check is completed

            print(f"Canvas element found for account {account_id}")
            return page, browser  # Return the browser and page objects
    except Exception as e:
        print(f"Error with account {account_id}: {e}")
        return None, None


def play_game(account_id, delay, page):
    if page:
        start_game(page, account_id, delay)
        wait_for_game_ready(page)
        while True:
            time.sleep(2)
            for x_offset, y_offset in canvas_coordinates:
                page.locator("#GameCanvas").click(
                    position={"x": x_offset, "y": y_offset})
                print(
                    f"Account {account_id} clicked at ({x_offset}, {y_offset})")
                time.sleep(0.5)


def wait_for_game_ready(page):
    retries = 0
    max_retries = 10
    while retries < max_retries:
        video_locator = page.locator("#Cocos2dGameContainer > video")
        if video_locator.is_visible():
            print("Video is visible. Game is not ready yet. Retrying...")
            retries += 1
            time.sleep(retries)
        else:
            print("Game is ready. No video detected.")
            break
    else:
        raise Exception(
            "Max retries reached. The game is not ready after multiple attempts.")


def wait_for_canvas_clickable(page):
    retries = 0
    max_retries = 10
    while retries < max_retries:
        try:
            page.locator("#GameCanvas").wait_for(state="visible", timeout=3000)
            page.locator("#GameCanvas").click(position={"x": 644, "y": 640})
            print("Canvas is visible and clickable.")
            break
        except Exception:
            retries += 1
            print(
                f"Attempt {retries}/{max_retries}: Canvas not clickable yet. Retrying...")
            time.sleep(retries)
    else:
        raise Exception(
            "Max retries reached. Canvas is not clickable after multiple attempts.")


def run_local_test_with_delay():
    with ThreadPoolExecutor(max_workers=TEST_ACCOUNTS) as executor:
        futures = []
        browsers = []

        # Open games for all accounts
        for account_id in range(TEST_ACCOUNTS):
            page, browser = executor.submit(
                open_game, account_id, START_DELAY).result()
            if page and browser:
                browsers.append(browser)
                futures.append(executor.submit(
                    play_game, account_id, START_DELAY, page))
                print(f"Account {account_id} waiting {START_DELAY} sec")

        # Wait for the user to confirm start
        prompt_for_start()

        # Wait until the start event is triggered
        start_event.wait()

        # Start the game for each account
        for future in futures:
            future.result()

        # Close browsers after game finishes
        for browser in browsers:
            browser.close()


if __name__ == "__main__":
    start_time = time.time()
    run_local_test_with_delay()
    print(f"Test completed in {time.time() - start_time:.2f} seconds")
