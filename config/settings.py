# config/settings.py
GAME_URL = "https://m13.ns86.kingmakergames.co/games/jackpot-jump/index.html?lang=en-US"

# Define click patterns for each account
PATTERNS = {
    'common': [
        (100, 150), (200, 300), (400, 500), (600, 700), (800, 900),
        # Add more coordinates for the 'common' pattern
    ],
    'special': [
        (50, 50), (100, 200), (300, 400), (500, 600), (700, 800),
        # Add more coordinates for the 'special' pattern
    ],
}
