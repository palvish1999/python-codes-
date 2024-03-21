import time
import sqlite3
from datetime import datetime
import random
import board
import busio
import digitalio
import adafruit_rfm9x
from tkinter import Tk, Frame, Button

# Define GPIO pin numbers
LORA_CS = board.GP5
LORA_RESET = board.GP6
RELAY_PINS = [board.GP7, board.GP8, board.GP9, board.GP10]  # Adjust these according to your relay wiring

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
    date = timestamp.strftime('%Y-%m-%d')
    time = timestamp.strftime('%H:%M:%S')
    c.execute("INSERT INTO relay_states (relay_num, state, date, time) VALUES (?, ?, ?, ?)",
              (relay_num, state, date, time))
    conn.commit()

# Function to control relay
def control_relay(relay_num, state):
    print(f"Relay {relay_num} is turned {state}")

# Function to handle button click event
def button_click(relay_num, state):
    control_relay(relay_num, state)
    update_relay_state(relay_num, state)
    print(f"Relay {relay_num} is turned {state}")

# Function to initialize LoRa communication
def init_lora():
    spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)  # Adjust these GPIO pins for SPI communication
    cs = digitalio.DigitalInOut(LORA_CS)
    reset = digitalio.DigitalInOut(LORA_RESET)
    rfM9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)
    return rfM9x

# Function to send command via LoRa
def send_lora_command(rfM9x, relay_num, state):
    message = f"Relay {relay_num} {state}"
    rfM9x.send(message)

# Function to create GUI
def create_gui():
    root = Tk()
    root.title("Relay Control")

    for i in range(4):
        relay_num = i + 1
        frame = Frame(root)
        frame.pack()

        on_button = Button(frame, text=f"Relay {relay_num} On", command=lambda num=relay_num: button_click(num, 'on'))
        on_button.pack(side="left")

        off_button = Button(frame, text=f"Relay {relay_num} Off", command=lambda num=relay_num: button_click(num, 'off'))
        off_button.pack(side="left")

    root.mainloop()

def main():
    try:
        print("Simulating sensor data and controlling relays. To exit, press Ctrl-C ")
        rfM9x = init_lora()
        create_gui()

    except KeyboardInterrupt:
        print("Program stopped")

if __name__ == '__main__':
    print("Press Ctrl-C to exit")
    main()
