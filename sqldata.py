import time
import sqlite3
from datetime import datetime
import random

# SQLite database initialization
conn = sqlite3.connect('relay_states.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS relay_states
             (id INTEGER PRIMARY KEY, relay_num INTEGER, state TEXT, date TEXT, time TEXT)''')
conn.commit()

# Function to update relay state in SQLite database
def update_relay_state(relay_num, state):
    timestamp = datetime.now()
    date = timestamp.strftime('%Y-%m-%d %H:%M:%S ')
    #time = timestamp.strftime('')
    c.execute("INSERT INTO relay_states (relay_num, state,  timestamp) VALUES (?, ?, ?)",
              (relay_num, state, date))
    conn.commit()

# Function to control relay
def control_relay(relay_num, state):
    # Your relay control logic goes here
    # This function will control the relay based on the relay number and state provided
    print(f"Relay {relay_num} is turned {state}")



def main():
    try:
        print("Simulating sensor data and controlling relays. To exit, press Ctrl-C ")
        for relay_num in range(1, 5):
                state = random.choice(['on', 'off'])
                control_relay(relay_num, state)
                update_relay_state(relay_num, state)
                print(f"Relay {relay_num} is turned {state}")
                time.sleep(5)

    except KeyboardInterrupt:
        print("Program stopped")

if __name__ == '__main__':
    print("Press Ctrl-C to exit")
    main()

