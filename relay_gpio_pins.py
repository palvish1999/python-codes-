import time
import pymssql
from datetime import datetime
import random
import RPi.GPIO as GPIO

# SQLite database initialization
SERVER = '192.168.1.16'
DATABASE = 'PunchData'
USERNAME = 'palvish'
PASSWORD = 'palvish'

# Establish a connection to the SQL Server
conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)

# Initialize GPIO
GPIO.setmode(GPIO.BOARD) # Use board pin numbering
RELAY_PINS = [11, 12, 13, 15] # Define GPIO pins for each relay
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)

# Function to update relay state in SQLite database
def update_relay_state(relay_num, state):
    cursor = conn.cursor()
    # Get current timestamp
    timestamp = datetime.now()
    print("Timestamp:", timestamp)  # Print the timestamp for verification
    # Define the SQL query to insert data into the relay_status table with timestamp
    sql_query = "INSERT INTO relay_status (relay_num, state, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(sql_query, (relay_num, state, timestamp))
    conn.commit()
    cursor.close()

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


