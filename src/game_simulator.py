# src/game_simulator.py

import time
from src.remote_executor import simulate_game_on_server
from config.config import TEST_ACCOUNTS, START_DELAY, servers


def start_game_simulation():
    """
    Start the simulation on remote servers.
    """
    # Loop through each server and account
    for account_id, server in enumerate(servers):
        delay = START_DELAY if account_id == 0 else 0
        simulate_game_on_server(server, account_id, delay)
