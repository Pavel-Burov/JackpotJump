import winrm
import time

# List of remote servers to connect to
servers = ["185.244.218.206"]  # Replace with actual server names or IPs

# Credentials to connect to the servers
username = "Administrator"  # Replace with your username
password = "Asas1234"  # Replace with your password

# Path to the Python script on the remote server
# Modify if the path is different
script_path = r"C:\Users\Administrator\Desktop\JackpotJump-main\local_test.py"

# Function to run the Python script on a remote server


def run_script_on_remote_server(server, script_path):
    try:
        # Create a session with the remote server using WinRM
        session = winrm.Session(
            f'http://{server}:5985/wsman',
            auth=(username, password),
            transport='ntlm',  # Use Kerberos authentication
            server_cert_validation='ignore'
        )

        # Command to run the Python script
        # Adjust the path to Python executable if necessary
        # Assumes Python is in the system PATH
        python_command = f"python {script_path}"
        powershell_command = f"""
        Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c {python_command}"
        """

        # Execute the PowerShell command on the remote server
        result = session.run_ps(powershell_command)

        # Check if the command ran successfully
        if result.status_code == 0:
            print(f"Successfully started the script on {server}.")
        else:
            print(
                f"Failed to start the script on {server}. Error: {result.std_err.decode()}")
    except Exception as e:
        print(f"Error connecting to {server}: {e}")


# Loop through all servers and run the script
for server in servers:
    run_script_on_remote_server(server, script_path)
    time.sleep(1)  # Sleep to avoid hitting the server too fast (optional)
