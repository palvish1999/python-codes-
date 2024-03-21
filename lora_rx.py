import RPi.GPIO as GPIO
from SX127x.LoRa import *
from SX127x.board_config import BOARD

# Set Raspberry Pi board configuration
#BOARD.setup()
GPIO.setwarnings(False)
# Initialize LoRa module
lora = LoRa()

# Initialize receiver parameters
frequency = 434e6  # Set your desired frequency (in Hz)
spreading_factor = 7
coding_rate = 5

# Set LoRa parameters
lora.set_mode(MODE.SLEEP)
lora.set_freq(frequency)
lora.set_spreading_factor(spreading_factor)
lora.set_coding_rate(coding_rate)
lora.set_pa_config(pa_select=1)

# Receive message
lora.start_rx()
print("Waiting for incoming message...")
lora.set_mode(MODE.RX)

while True:
    if lora.received_packet():
        payload = lora.read_payload()
        print("Received message:", payload)
        break

# Clean up GPIO
GPIO.cleanup()
