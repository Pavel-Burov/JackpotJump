# src/server_manager.py
import subprocess
from config.settings import GAME_URL


def run_automation_on_server(server_ip: str):
    """
    Runs the automation script on a remote server using PowerShell Remoting.
    """
    command = f"Invoke-Command -ComputerName {server_ip} -ScriptBlock {{ python C:\\path\\to\\game_automation.py }} -Credential (Get-Credential)"
    print(f"Running automation on server {server_ip}...")

    # Run the command to start the automation script on the remote server
    result = subprocess.run(command, shell=True, capture_output=True)
    print(f"Output from {server_ip}: {result.stdout.decode()}")
    if result.stderr:
        print(f"Error: {result.stderr.decode()}")


def run_on_multiple_servers(servers: list):
    """
    Run the automation script on multiple remote servers.
    """
    for server in servers:
        run_automation_on_server(server)


if __name__ == "__main__":
    # List of your Windows server IPs or hostnames
    servers = ['Server1_IP', 'Server2_IP', 'Server3_IP', 'Server4_IP', 'Server5_IP',
               'Server6_IP', 'Server7_IP', 'Server8_IP', 'Server9_IP', 'Server10_IP']

    # Run automation on all servers
    run_on_multiple_servers(servers)
