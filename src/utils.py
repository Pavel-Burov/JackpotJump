# src/utils.py
import logging
import time


def setup_logging():
    """
    Set up logging configuration.
    """
    logging.basicConfig(
        filename='logs/automation.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )


def log_error(message):
    """
    Log error message to the log file.
    """
    logging.error(message)

# src/utils.py


def wait_for_seconds(seconds):
    """
    Utility function to pause execution for a specified amount of time.
    """
    time.sleep(seconds)
