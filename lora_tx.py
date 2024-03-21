import RPi.GPIO as GPIO
from SX127x.LoRa import *
from SX127x.board_config import BOARD

# Set Raspberry Pi board configuration
BOARD.setup()

# Initialize LoRa module
lora = LoRa()

# Initialize sender parameters
sender_message = "Hello, LoRa World!"
frequency = 434e6  # Set your desired frequency (in Hz)
spreading_factor = 7
coding_rate = 5
calibration_freq = 868e6

# Set LoRa parameters
#lora.set_mode(MODE.SLEEP)
lora.set_freq(frequency)
lora.set_spreading_factor(spreading_factor)
lora.set_coding_rate(coding_rate)
lora.set_pa_config(pa_select=1)
lora.set_mode(MODE.FSK_STDBY)
# Send message
lora.start_tx()
lora.write_payload(sender_message)
lora.set_mode(MODE.TX)

lora.tx_chain_calibration(calibration_freq)

print("Message sent:", sender_message)

# Clean up GPIO
GPIO.cleanup()


