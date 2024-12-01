# main.py
from src.server_manager import launch_all_servers
from src.timer import wait_for_countdown
from src.utils import setup_logging


def main():
    setup_logging()
    print("Starting the automation process.")

    # Wait for countdown before starting the automation
    wait_for_countdown()

    # Launch all servers (200 windows across 10 servers)
    launch_all_servers()


if __name__ == "__main__":
    main()
