import winrm
import time
import sys
import io
from config.config import servers, START_DELAY, TEST_ACCOUNTS
from concurrent.futures import ThreadPoolExecutor

# Set default encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def create_winrm_session(server):
    """
    Establish a WinRM session to the remote server with NTLM authentication.
    """
    session = winrm.Session(
        f'http://{server["hostname"]}:5985/wsman',
        auth=(server["username"], server["password"]),
        transport='ntlm'  # Use NTLM authentication
    )
    return session


def execute_remote_script(session, account_id, delay):
    """
    Executes the play_game.py script remotely using WinRM.
    """
    try:
        # Correct the string formatting for the command
        script = f'python C:\\Users\\Administrator\\Desktop\\JackpotJump-main\\play_game.py {account_id} {delay}'

        # Execute the script remotely
        result = session.run_cmd(script)

        # Print the result of the remote command
        print(f"Executed on {session}: {result.std_out.decode()}")

        # Check for errors in the command execution
        if result.std_err:
            print(f"Error on {session}: {result.std_err.decode()}")

    except Exception as e:
        print(f"Error executing script on {session}: {str(e)}".encode('utf-8'))


def start_game_on_servers():
    """
    Start the game simulation on all remote servers.
    """
    with ThreadPoolExecutor(max_workers=TEST_ACCOUNTS) as executor:
        futures = []

        # Submit the task for each account on each server
        for account_id, server in enumerate(servers):
            delay = START_DELAY if account_id == 0 else 0
            # Create the session for each server
            session = create_winrm_session(server)
            futures.append(executor.submit(
                execute_remote_script, session, account_id, delay))

        # Wait for all tasks to finish and collect results
        for future in futures:
            future.result()


if __name__ == "__main__":
    start_game_on_servers()
