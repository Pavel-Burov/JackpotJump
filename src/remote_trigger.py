# src/remote_trigger.py
import winrm


def run_remote_script(server_ip: str, script_path: str):
    """
    Connects to a Windows server and runs the specified script via WinRM.
    """
    session = winrm.Session(
        f'http://{server_ip}:5985/wsman', auth=('username', 'password'))
    command = f'python {script_path}'

    result = session.run_cmd(command)
    print(f"Output from {server_ip}: {result.std_out.decode()}")
    if result.stderr:
        print(f"Error: {result.stderr.decode()}")


def run_on_multiple_servers(servers: list, script_path: str):
    """
    Run a Python script on multiple remote servers using WinRM.
    """
    for server in servers:
        run_remote_script(server, script_path)


if __name__ == "__main__":
    # List of Windows servers and the path to the game automation script
    servers = ['Server1_IP', 'Server2_IP', 'Server3_IP', 'Server4_IP', 'Server5_IP',
               'Server6_IP', 'Server7_IP', 'Server8_IP', 'Server9_IP', 'Server10_IP']

    script_path = r'C:\path\to\game_automation.py'

    # Run automation script on all servers
    run_on_multiple_servers(servers, script_path)
