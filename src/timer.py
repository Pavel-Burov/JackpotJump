# src/timer.py
import time
from config.settings import COUNTDOWN_TIME


def wait_for_countdown():
    """
    Wait for the countdown before starting the next round.
    """
    print(f"Waiting for {COUNTDOWN_TIME} seconds...")
    time.sleep(COUNTDOWN_TIME)
    print("Countdown finished, starting next round!")
