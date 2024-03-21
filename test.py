import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

# Set the GPIO pin for relay
relay_pin = 19

# Set relay pin as output
GPIO.setup(relay_pin, GPIO.OUT)

try:
    while True:
        # Turn the relay ON (high)
        GPIO.output(relay_pin, GPIO.HIGH)
        print("Relay ON")
        time.sleep(10)  # Wait for 1 second

        # Turn the relay OFF (low)
        GPIO.output(relay_pin, GPIO.LOW)
        print("Relay OFF")
        time.sleep(10)  # Wait for 1 second

except KeyboardInterrupt:
    print("Exiting program")

finally:
    # Clean up GPIO
    GPIO.cleanup()
