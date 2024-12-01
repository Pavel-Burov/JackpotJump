import time
from playwright.sync_api import Playwright, sync_playwright
from concurrent.futures import ThreadPoolExecutor
import signal
import sys

# Configuration settings
TEST_ACCOUNTS = 2  # Number of accounts to test (local test)
START_DELAY = 45  # Delay for the first account to wait before others start

# Coordinates for the GameCanvas clicks (replace with your actual values)
canvas_coordinates = [
    (580, 600),
    (580, 535),
    (580, 465),
    (580, 400),
    (580, 330),
    (580, 260),
]


def start_game(page, account_id, delay):
    # Logic to click the start button for the first account
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
        time.sleep(delay)  # Simulate the wait for the first account
    else:
        print(f"Account {account_id} waiting for {delay} seconds...")
        time.sleep(delay)  # Other accounts wait for 45 seconds
        page.locator("#GameCanvas").click(position={"x": 669, "y": 642})
        time.sleep(0.5)
        page.locator("#GameCanvas").click(position={"x": 757, "y": 520})
        time.sleep(0.5)
        page.locator("#GameCanvas").click(position={"x": 635, "y": 421})
        time.sleep(0.5)
        page.locator("#GameCanvas").click(position={"x": 635, "y": 421})
        print(f"Account {account_id} clicked the start button.")


# Function to handle the game interaction for each account
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

            # Check if the game is ready and click the start button
            wait_for_game_ready(page)

            # Game logic
            time.sleep(2)
            for x_offset, y_offset in canvas_coordinates:
                page.locator("#GameCanvas").click(
                    position={"x": x_offset, "y": y_offset})
                print(
                    f"Account {account_id} clicked at ({x_offset}, {y_offset})")
                # Delay between clicks to simulate human behavior
                time.sleep(0.5)

            time.sleep(50)
            # Close the browser after completing the pattern
            context.close()
            browser.close()
    except Exception as e:
        print(f"Error with account {account_id}: {e}")


# Function to handle the check for game readiness (wait for video to disappear)
def wait_for_game_ready(page):
    """
    Checks if the game is ready to play. If a video is present, waits for it to disappear.
    """
    retries = 0
    max_retries = 10  # Limit the number of retries
    while retries < max_retries:
        # Check if the video is visible
        video_locator = page.locator("#Cocos2dGameContainer > video")
        if video_locator.is_visible():
            print("Video is visible. Game is not ready yet. Retrying...")
            retries += 1
            time.sleep(retries)  # Exponentially increase delay before retry
        else:
            print("Game is ready. No video detected.")
            break  # Exit loop once the game is ready
    else:
        raise Exception(
            "Max retries reached. The game is not ready after multiple attempts.")


# Graceful shutdown handler (Ctrl + C)
def signal_handler(sig, frame):
    print("\nGracefully stopping the script...")
    sys.exit(0)


# Register the signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)


# Function to wait until the GameCanvas is visible and clickable
def wait_for_canvas_clickable(page):
    """
    Waits for the #GameCanvas element to be visible and clickable.
    Retries if the element is not immediately clickable.
    """
    retries = 0
    max_retries = 10  # Limit the number of retries
    while retries < max_retries:
        try:
            # Wait for the canvas to be visible first
            page.locator("#GameCanvas").wait_for(state="visible", timeout=3000)
            # Now attempt to click on the canvas
            page.locator("#GameCanvas").click(position={"x": 644, "y": 640})
            print("Canvas is visible and clickable.")
            break  # Exit the loop once the click is successful
        except Exception as e:
            retries += 1
            print(
                f"Attempt {retries}/{max_retries}: Canvas not clickable yet. Retrying in {retries} seconds...")
            time.sleep(retries)  # Exponentially increase the retry delay
    else:
        # If we reach max retries, raise an exception
        raise Exception(
            "Max retries reached. Canvas is not clickable after multiple attempts.")


# Function to run the local test with delays
def run_local_test_with_delay():
    """
    Run the local test for a specified number of accounts (simulating gameplay in parallel).
    - First account starts and waits for 45 seconds.
    - All other accounts start simultaneously after the delay.
    """
    with ThreadPoolExecutor(max_workers=TEST_ACCOUNTS) as executor:
        # Submit the first account with a 45-second delay
        futures = [executor.submit(open_game_and_play, 0, START_DELAY)]

        # Submit the rest of the accounts (they will start simultaneously after the delay)
        for account_id in range(1, TEST_ACCOUNTS):
            futures.append(executor.submit(
                open_game_and_play, account_id, START_DELAY))
            print(f"Account {account_id} waiting {START_DELAY}")

        # Wait for all futures to complete
        for future in futures:
            future.result()  # Wait for the task to complete and catch any exceptions


if __name__ == "__main__":
    start_time = time.time()
    run_local_test_with_delay()
    print(f"Test completed in {time.time() - start_time:.2f} seconds")
