# src/game_interaction.py
from playwright.sync_api import Page, sync_playwright
from config.settings import GAME_URL, PATTERNS


def open_game_and_play(account_id: int):
    """
    Opens the game for the specified account and simulates gameplay actions.
    """
    with sync_playwright() as p:
        # Launch the browser (Headless mode: False means GUI, True means headless)
        # Set to True for headless mode
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to the game
        page.goto(GAME_URL)
        print(f"Game opened for account {account_id}")

        # Choose the correct pattern for the account
        pattern = PATTERNS['common'] if account_id < 184 else PATTERNS['special']

        # Click on the canvas at specified coordinates for the game
        for x, y in pattern:
            click_on_canvas(page, x, y)

        # Close the browser after playing
        browser.close()


def click_on_canvas(page: Page, x_offset: int, y_offset: int):
    """
    Click on the game canvas at specified coordinates relative to the canvas.
    """
    bbox = page.query_selector('#GameCanvas').bounding_box()
    if bbox:
        x = bbox['x'] + x_offset
        y = bbox['y'] + y_offset
        page.mouse.click(x, y)
        print(f"Clicked on canvas at ({x}, {y})")


if __name__ == "__main__":
    for account_id in range(200):
        open_game_and_play(account_id)
