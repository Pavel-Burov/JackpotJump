# run_test.py

import time
from concurrent.futures import ThreadPoolExecutor
from src.game_simulator import start_game_simulation
from config.config import TEST_ACCOUNTS


def run_remote_tests():
    """
    Run the remote tests with parallel execution on multiple servers.
    """
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=TEST_ACCOUNTS) as executor:
        futures = []

        # Submit tasks to run the simulation for each account on a different server
        for i in range(TEST_ACCOUNTS):
            futures.append(executor.submit(start_game_simulation))

        # Wait for all tasks to complete
        for future in futures:
            future.result()  # Blocks until the task is finished

    print(f"Test completed in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    run_remote_tests()
