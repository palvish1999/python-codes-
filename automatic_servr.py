import paramiko
import sqlite3
import os

# Raspberry Pi SSH connection details
hostname = '192.168.1.178'
port = 27017
username = 'pi'
password = 'raspberry'  # Replace with your Raspberry Pi's password
remote_db_path = '/path/to/remote/database.db'

# Windows local directory to stre the transferred database file
local_dir = 'C:/Users/s.palvish/Documents'

# Establish SSH connection to Raspberry Pi
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh_client.connect(hostname, port, username, password)
    print("SSH connection established.")

    # Transfer the SQLite database file from Raspberry Pi to Windows
    sftp_client = ssh_client.open_sftp()
    sftp_client.get(remote_db_path, os.path.join(local_dir, 'database.db'))
    print("Database file transferred successfully.")

    # Establish SQLite connection to the transferred database file
    db_conn = sqlite3.connect(os.path.join(local_dir, 'database.db'))
    cursor = db_conn.cursor()

    # Example: Execute a query on the transferred database
    cursor.execute("SELECT * FROM your_table")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close SQLite connection
    db_conn.close()

    # Close SFTP connection
    sftp_client.close()

except paramiko.AuthenticationException:
    print("Authentication failed, please check your credentials.")
except paramiko.SSHException as ssh_exc:
    print("Unable to establish SSH connection:", str(ssh_exc))
finally:
    # Close SSH connection
    ssh_client.close()
