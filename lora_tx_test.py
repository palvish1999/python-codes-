import RPi.GPIO as GPIO
from SX127x.LoRa import LoRa
import time

# GPIO pin for LoRa reset
RESET_PIN = 12

# Set up LoRa module
lora = LoRa()
lora.set_mode(LoRa.SLEEP_MODE)
lora.set_pa_config(pa_select=1)
lora.set_freq(433.0)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RESET_PIN, GPIO.OUT)

# Reset LoRa module
GPIO.output(RESET_PIN, GPIO.HIGH)
time.sleep(0.1)
GPIO.output(RESET_PIN, GPIO.LOW)
time.sleep(0.1)

# Message to send
message = "Hello Pi 4!"

# Send message
lora.send_message(message)
print("Message sent:", message)

# Cleanup
lora.set_mode(LoRa.SLEEP_MODE)
GPIO.cleanup()
