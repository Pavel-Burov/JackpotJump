# central-controller/controller.py
from concurrent.futures import ThreadPoolExecutor
import winrm
import time
from config.config import servers, START_DELAY, TEST_ACCOUNTS


def create_winrm_session(server):
    """
    Establish a WinRM session to the remote server.
    """
    session = winrm.Session(
        f'http://{server["hostname"]}:5985/wsman',
        auth=(server["username"], server["password"]),
    )
    return session


def execute_remote_script(session, account_id, delay):
    """
    Executes the play_game.py script remotely using WinRM.
    """
    script = f'python C:\\path\\to\\play_game.py {account_id} {delay}'  # Adjust the path
    result = session.run_cmd(script)
    print(f"Executed on {session}: {result.std_out.decode()}")


def start_game_on_servers():
    """
    Start the game simulation on all remote servers.
    """
    with ThreadPoolExecutor(max_workers=TEST_ACCOUNTS) as executor:
        futures = []

        # Submit the task for each server
        for account_id, server in enumerate(servers):
            delay = START_DELAY if account_id == 0 else 0
            session = create_winrm_session(server)
            futures.append(executor.submit(
                execute_remote_script, session, account_id, delay))

        # Wait for all tasks to finish
        for future in futures:
            future.result()


if __name__ == "__main__":
    start_game_on_servers()
