import RPi.GPIO as GPIO
import time, sys

# GPIO pins for flow sensors
FLOW_SENSOR_GPIO_IN = 26
FLOW_SENSOR_GPIO_OUT = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FLOW_SENSOR_GPIO_OUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Global variables to count pulses for each sensor
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

while True:
    try:
        # Reset pulse counts and start counting
        count_in = 0
        count_out = 0

        # Sleep for 1 second to count pulses
        time.sleep(1)

        # Get flow rates for inflow and outflow
        flow_in = count_in / 7.5  # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min
        flow_out = count_out / 7.5

        # Print flow rates
        print("Inflow: %.3f Liter/min" % flow_in)
        print("Outflow: %.3f Liter/min" % flow_out)

        # Sleep for 5 seconds before next reading
        time.sleep(5)

    except KeyboardInterrupt:
        print('\nkeyboard interrupt!')
        GPIO.cleanup()
        sys.exit()