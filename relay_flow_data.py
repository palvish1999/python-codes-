import RPi.GPIO as GPIO
import time
import datetime
import pymssql

# MySQL Database Configuration
SERVER = '192.168.1.102'
DATABASE = 'PunchData'
USERNAME = 'palvish'
PASSWORD = 'palvish'

# GPIO Pins for Relays
RELAY_PINS = [17, 18, 27, 22]  # Example GPIO pins, adjust as needed

# GPIO Pins for Flow Sensors
FLOW_SENSOR_PINS = [23, 24]  # Example GPIO pins, adjust as needed

# Relay numbering
RELAY_NUMBERS = ['Relay 1', 'Relay 2', 'Relay 3', 'Relay 4']

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

# Initialize Flow Sensors
for pin in FLOW_SENSOR_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to read flow from sensor
def read_flow(pin):
    count = 0
    try:
        while GPIO.input(pin) == GPIO.LOW:
            count += 1
            time.sleep(0.0001)
        # Convert count to liters per minute (adjust conversion factor as needed)
        liters_per_minute = count * 10  # Example conversion factor
        return liters_per_minute
    except KeyboardInterrupt:
        GPIO.cleanup()

# Function to insert data into SQL Server database
def insert_data(relay_num, flow_in, flow_out):
    try:
        conn = pymssql.connect(host=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
        cursor = conn.cursor()
        query = "INSERT INTO your_table_name (relay_num, flow_in, flow_out, updated_on) VALUES (%s, %s, %s, %s)"
        data = (relay_num, flow_in, flow_out, datetime.datetime.now())
        cursor.execute(query, data)
        conn.commit()
        print("Data inserted successfully!")
    except pymssql.Error as error:
        print("Error:", error)
    finally:
        if conn:
            cursor.close()
            conn.close()

try:
    while True:
        print("Select an option:")
        print("1. Turn ON all relays")
        print("2. Turn OFF all relays")
        print("3. Individual control")
        user_input = input("Enter your choice (1/2/3): ")

        if user_input == '1':
            for pin in RELAY_PINS:
                GPIO.output(pin, GPIO.HIGH)
        elif user_input == '2':
            for pin in RELAY_PINS:
                GPIO.output(pin, GPIO.LOW)
        elif user_input == '3':
            print("Select relay to control:")
            for i, relay_num in enumerate(RELAY_NUMBERS, 1):
                print(f"{i}. {relay_num}")

            relay_choice = int(input("Enter relay number to control (1-4): "))
            if 1 <= relay_choice <= 4:
                pin_index = relay_choice - 1
                pin = RELAY_PINS[pin_index]

                print(f"Selected {RELAY_NUMBERS[pin_index]}:")
                sub_input = input("Enter '1' to turn ON or '0' to turn OFF: ")
                if sub_input == '1':
                    GPIO.output(pin, GPIO.HIGH)
                elif sub_input == '0':
                    GPIO.output(pin, GPIO.LOW)

        # Read flow data
        flow_in = read_flow(FLOW_SENSOR_PINS[0])
        flow_out = read_flow(FLOW_SENSOR_PINS[1])

        # Insert data into database
        insert_data(f"Relay {relay_choice}", flow_in, flow_out)

        time.sleep(1)  # Adjust as needed

except KeyboardInterrupt:
    GPIO.cleanup()
