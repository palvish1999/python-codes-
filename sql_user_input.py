import time
import sqlite3
from datetime import datetime
import random

# SQLite database initialization
conn = sqlite3.connect('relay_states.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS relay_states
             (id INTEGER PRIMARY KEY, relay_num INTEGER, state TEXT, date TEXT, time TEXT)''') #data table creation
conn.commit()

# Function to update relay state in SQLite database
def update_relay_state(relay_num, state):
    timestamp = datetime.now()
    date = timestamp.strftime('%Y-%m-%d %H:%M:%S') #date and time addon for data base 
    #time = timestamp.strftime('')
    c.execute("INSERT INTO relay_states (relay_num, state, timestamp) VALUES (?, ?, ?)", #inserting values for database .db file
              (relay_num, state, date))
    conn.commit()

# Function to control relay
def control_relay(relay_num, state):
    # Your relay control logic goes here
    # This function will control the relay based on the relay number and state provided
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

if __name__ == '__main__':
    print("Press Ctrl-C to exit")
    main()
