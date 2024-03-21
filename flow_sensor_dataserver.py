import RPi.GPIO as GPIO
import time
import pymssql

FLOW_SENSOR_GPIO_IN = 26
FLOW_SENSOR_GPIO_OUT = 21

# Define the SQL Server connection parameters
SERVER = '192.168.1.16'
DATABASE = 'PunchData'
USERNAME = 'palvish'
PASSWORD = 'palvish'

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FLOW_SENSOR_GPIO_OUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

count_in = 0
count_out = 0

def countPulseIn(channel):
    global count_in
    count_in += 1

def countPulseOut(channel):
    global count_out
    count_out += 1

GPIO.add_event_detect(FLOW_SENSOR_GPIO_IN, GPIO.FALLING, callback=countPulseIn)
GPIO.add_event_detect(FLOW_SENSOR_GPIO_OUT, GPIO.FALLING, callback=countPulseOut)

try:
    conn = pymssql.connect(host=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
    cursor = conn.cursor()

    while True:
        try:
            count_in = 0
            count_out = 0
            time.sleep(1)

            flow_in = count_in / 7.5
            flow_out = count_out / 7.5

            flow_in_str = "{:.2f}".format(flow_in)
            flow_out_str = "{:.2f}".format(flow_out)

            print("Inflow: {} Liter/min".format(flow_in_str))
            print("Outflow: {} Liter/min".format(flow_out_str))

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            insert_query = "INSERT INTO pump_flow_data (flow_in, flow_out, timestamp) VALUES (%s, %s, %s)"
            insert_values = (flow_in, flow_out, timestamp)
            cursor.execute(insert_query, insert_values)
            conn.commit()

            time.sleep(5)
            
        except KeyboardInterrupt:
            print('\nkeyboard interrupt!')
            break
        except pymssql.Error as e:
            print(f"Error: {e}")
            conn.rollback()

finally:
    if 'conn' in locals() and conn.open:
        cursor.close()
        conn.close()
        print("SQL Server connection is closed.")
    GPIO.cleanup()
