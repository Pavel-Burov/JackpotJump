import time
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor
import threading
import signal
import sys
import math
import tkinter as tk

# Configuration settings
TEST_ACCOUNTS = 4  # Number of accounts to test (adjust as needed)

# Coordinates for the GameCanvas clicks (replace with your actual values)
canvas_coordinates = [
    (580, 600),
    (580, 535),
    (580, 465),
    (580, 400),
    (580, 330),
    (580, 260),
]


class SharedState:
    """
    Class to manage shared state across threads.
    """

    def __init__(self, total_accounts):
        self.ready_count = 0
        self.total_accounts = total_accounts
        self.lock = threading.Lock()
        self.all_ready_event = threading.Event()
        self.start_event = threading.Event()


def get_screen_size():
    """
    Retrieves the screen width and height using tkinter.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height


def wait_for_splash_screen_to_disappear(page):
    """
    Waits for the splash screen to disappear.
    """
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
            break
    else:
        print("Splash screen didn't disappear after retries.")


def start_game(page, account_id):
    """
    Simulates clicking actions to start the game.
    """
    # Clicking on the game to start
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


def prompt_for_start():
    """
    Prompts the user to start the game. This is only called once after all accounts are ready.
    """
    while True:
        start_input = input("Start all accounts? (y/n): ").strip().lower()
        if start_input == 'y':
            return True
        elif start_input == 'n':
            print("Game not started. Exiting...")
            sys.exit(0)
        else:
            print("Invalid input. Please enter 'y' to start or 'n' to exit.")


def open_game_and_play(account_id: int, shared_state: SharedState, window_width: int, window_height: int, window_x: int, window_y: int):
    """
    Handles the game interaction for each account.
    """
    try:
        with sync_playwright() as p:
            # Launch the browser with specific window size and position
            browser = p.chromium.launch(
                headless=False,
                args=[
                    f'--window-size={window_width},{window_height}',
                    f'--window-position={window_x},{window_y}'
                ]
            )
            context = browser.new_context(
                # Example permissions; adjust as needed
                permissions=['geolocation', 'notifications']
            )
            page = context.new_page()

            # Navigate to the game page
            page.goto(
                "https://cdn.kingdomhall729.com/qat/jackpot-jump/2024-11-22-13-44-55/index.html?currency=THB")

            # Wait for the splash screen to disappear
            wait_for_splash_screen_to_disappear(page)

            # Wait for the #GameCanvas element to be present and visible
            wait_for_canvas_clickable(page)
            print(f"Canvas element found for account {account_id}")

            # Signal readiness
            with shared_state.lock:
                shared_state.ready_count += 1
                print(
                    f"Account {account_id} is ready. Total ready: {shared_state.ready_count}/{shared_state.total_accounts}")
                if shared_state.ready_count == shared_state.total_accounts:
                    shared_state.all_ready_event.set()

            # Wait until the start_event is set
            shared_state.start_event.wait()

            if shared_state.start_event.is_set():
                print(f"Account {account_id} is starting the game.")
                # Start the game actions
                start_game(page, account_id)

                # Adjust the viewport size to fit within the window
                # To ensure content fits, reduce viewport size slightly
                adjusted_width = window_width - 100
                adjusted_height = window_height - 100
                page.set_viewport_size(
                    {"width": adjusted_width, "height": adjusted_height})

                # Game loop for gameplay actions
                while True:
                    # Game logic: click on the game canvas
                    time.sleep(2)
                    for x_offset, y_offset in canvas_coordinates:
                        page.locator("#GameCanvas").click(
                            position={"x": x_offset, "y": y_offset})
                        print(
                            f"Account {account_id} clicked at ({x_offset}, {y_offset})")
                        # Delay between clicks to simulate human behavior
                        time.sleep(0.5)

    except Exception as e:
        print(f"Error with account {account_id}: {e}")


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


def run_local_test():
    """
    Runs the local test for a specified number of accounts (simulating gameplay in parallel).
    All accounts start after the user confirms to start.
    """
    shared_state = SharedState(TEST_ACCOUNTS)

    # Get screen size
    screen_width, screen_height = get_screen_size()
    print(f"Screen size: {screen_width}x{screen_height}")

    # Define usable width (left 2/3 of the screen)
    usable_width = (screen_width * 2) // 3
    usable_height = screen_height  # Full height

    # Compute window size
    window_width = usable_width // TEST_ACCOUNTS
    window_height = usable_height // TEST_ACCOUNTS
    print(f"Each window size: {window_width}x{window_height}")

    # Define offset for overlapping
    offset_x = 100  # pixels to shift right for each window
    offset_y = 100  # pixels to shift down for each window

    with ThreadPoolExecutor(max_workers=TEST_ACCOUNTS) as executor:
        # Submit the accounts to the executor
        for account_id in range(TEST_ACCOUNTS):
            # Compute window position with overlap
            window_x = account_id * offset_x
            window_y = account_id * offset_y

            # Ensure windows do not exceed usable screen area
            if window_x + window_width > usable_width:
                window_x = usable_width - window_width
            if window_y + window_height > usable_height:
                window_y = usable_height - window_height

            print(
                f"Launching Account {account_id} at position ({window_x}, {window_y})")

            # Submit the task with window size and position
            executor.submit(
                open_game_and_play,
                account_id,
                shared_state,
                window_width,
                window_height,
                window_x,
                window_y
            )
            print(f"Account {account_id} submitted to executor.")

        # Wait until all accounts are ready
        shared_state.all_ready_event.wait()
        print("All accounts are ready.")

        # Prompt the user once
        if prompt_for_start():
            # Set the start_event to let all threads proceed
            shared_state.start_event.set()
            print("Start event set. All accounts will start the game.")
        else:
            print("Start event not set. Exiting...")
            sys.exit(0)

        # Since the game loops are infinite, the script will keep running
        # Implement a mechanism to stop the threads gracefully if needed


if __name__ == "__main__":
    start_time = time.time()
    run_local_test()
    print(f"Test completed in {time.time() - start_time:.2f} seconds")
