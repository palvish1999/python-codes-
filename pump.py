import RPi.GPIO as GPIO
from pymongo import MongoClient
import datetime

GPIO.setwarnings(False)

# MongoDB Compass connection details
mongo_uri = "mongodb://192.168.1.16:27017"
database_name = "Pumpsdata"
collection_name = "relay_states"

# Initialize GPIO
relay_pin = 19  # Example GPIO pin for the relay
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

# MongoDB Compass client
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

def switch_relay(state):
    GPIO.output(relay_pin, state)
    current_time = datetime.datetime.now()
    collection.insert_one({"timestamp": current_time, "state": state})

try:
    while True:
        user_input = input("Enter 'on' to switch on the relay, 'off' to switch off, or 'exit' to quit: ")
        if user_input == "on":
            switch_relay(GPIO.HIGH)  # Switch on the relay
            print("Relay switched ON")
        elif user_input == "off":
            switch_relay(GPIO.LOW)  # Switch off the relay
            print("Relay switched OFF")
        elif user_input == "exit":
            break
        else:
            print("Invalid input. Please enter 'on', 'off', or 'exit'.")

finally:
    GPIO.cleanup()
