# src/utils.py
import logging


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
