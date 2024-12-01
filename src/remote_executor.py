# src/remote_executor.py

import winrm
from config.config import servers
import time
import logging

logging.basicConfig(level=logging.INFO)


def create_winrm_session(server):
    """
    Establishes a WinRM session for the given server.
    """
    try:
        session = winrm.Session(
            f"http://{server['hostname']}:5985/wsman",
            auth=(server['username'], server['password'])
        )
        logging.info(f"Connected to {server['hostname']}")
        return session
    except Exception as e:
        logging.error(f"Failed to connect to {server['hostname']}: {e}")
        return None


def execute_remote_command(session, command):
    """
    Executes a command on the remote server.
    """
    try:
        result = session.run_cmd(command)
        logging.info(f"Command executed on server: {result.std_out.decode()}")
        return result
    except Exception as e:
        logging.error(f"Error executing command: {e}")
        return None


def simulate_game_on_server(server, account_id, delay):
    """
    Simulate game actions on a remote server.
    """
    session = create_winrm_session(server)
    if not session:
        return

    try:
        # Example: command to simulate game action
        commands = f"""
        # Simulate gameplay for Account {account_id}
        echo Starting game for Account {account_id}
        timeout /t {delay} /nobreak
        echo Account {account_id} completed actions.
        """

        # Execute the simulation command
        execute_remote_command(session, commands)

        # Simulate the gameplay (clicks and delays)
        time.sleep(2)  # Wait a bit before starting clicks
        for x_offset, y_offset in server['canvas_coordinates']:
            logging.info(
                f"Account {account_id} clicks at ({x_offset}, {y_offset}) on {server['hostname']}")
            time.sleep(0.5)  # Simulating human behavior with a delay

        logging.info(
            f"Game simulation completed for Account {account_id} on {server['hostname']}")

    except Exception as e:
        logging.error(
            f"Error during simulation for account {account_id} on {server['hostname']}: {e}")
