import time
import sqlite3
from datetime import datetime
import random
import RPi.GPIO as GPIO
import paramiko
import os

# SQLite database initialization
conn = sqlite3.connect('relay_states.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS relay_states
             (id INTEGER PRIMARY KEY, relay_num INTEGER, state TEXT, date TEXT, time TEXT)''') #data table creation
conn.commit()

# Raspberry Pi SSH connection details
hostname = '192.168.1.178'
port = 22
username = 'pi'
password = 'raspberry'  # Replace with your Raspberry Pi's password
remote_db_path = '/home/pi/relay_states.db'

# Windows local directory to store the transferred database file
local_dir = 'C:/Users/s.palvish/Documents/relay_states'

# Function to update relay state in SQLite database
def update_relay_state(relay_num, state):
    timestamp = datetime.now()
    date = timestamp.strftime('%Y-%m-%d %H:%M:%S') #date and time addon for data base 
    c.execute("INSERT INTO relay_states (relay_num, state, date, time) VALUES (?, ?, ?, ?)",
              (relay_num, state, date, timestamp.time().isoformat()))
    conn.commit()

# Function to control relay
def control_relay(relay_num, state):
    pin = RELAY_PINS[relay_num - 1]
    if state == 'on':
        GPIO.output(pin, GPIO.HIGH) # Turn relay on
    elif state == 'off':
        GPIO.output(pin, GPIO.LOW) # Turn relay off
    print(f"Relay {relay_num} is turned {state}")

# Function to get user input for relay control
def get_user_input():
    while True:
        try:
            relay_num = int(input("Enter relay number (1-4): "))
            if relay_num < 1 or relay_num > 4:
                print("Invalid relay number. Please enter a number between 1 and 4.")
                continue
            
            state = input("Enter state (on/off): ").lower()
            if state not in ['on', 'off']:
                print("Invalid state. Please enter 'on' or 'off'.")
                continue
            
            return relay_num, state
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Initialize GPIO
GPIO.setmode(GPIO.BOARD) # Use board pin numbering
RELAY_PINS = [11, 12, 13, 15] # Define GPIO pins for each relay
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)

# Establish SSH connection to Raspberry Pi
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh_client.connect(hostname, port, username, password)
    print("SSH connection established.")

    # Transfer the SQLite database file from Raspberry Pi to Windows
    sftp_client = ssh_client.open_sftp()
    sftp_client.get(remote_db_path, os.path.join(local_dir, 'relay_states'))
    print("Database file transferred successfully.")

    # Establish SQLite connection to the transferred database file
    db_conn = sqlite3.connect(os.path.join(local_dir, 'relay_states.db'))
    cursor = db_conn.cursor()

    # Example: Execute a query on the transferred database
    cursor.execute("SELECT * FROM relay_states")
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

def main():
    try:
        print("Simulating sensor data and controlling relays. To exit, press Ctrl-C ")

        while True:
            # Get user input for relay control
            relay_num, state = get_user_input()
            
            # Control relay based on user input
            control_relay(relay_num, state)
            update_relay_state(relay_num, state)
            print(f"Relay {relay_num} is turned {state}")

    except KeyboardInterrupt:
        print("Program stopped")
        GPIO.cleanup() # Cleanup GPIO pins

if __name__ == '__main__':
    print("Press Ctrl-C to exit")
    main()
