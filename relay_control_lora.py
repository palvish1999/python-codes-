import time
from SX127x.LoRa import *
import RPi.GPIO as GPIO

# GPIO pin mapping
DIO0 = 11

# Define GPIO pins for relay control
RELAY_PINS = [13, 15, 16, 18]  # Example relay pins (modify as needed)

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        #RELATsuper(LoRaReceiver, self).__init__(verbose)
        self.setup_gpio()
        self.set_mode(MODE.STDBY)

    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(DIO0, GPIO.IN)

        # Set up relay pins as outputs
        for pin in RELAY_PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)  # Initialize relays to OFF state

    def on_rx_done(self):
        #self.set_mode(MODE.STDBY)
        payload = self.read_payload()
        print("Received: {}".format(payload))

        # Process relay control based on received message
        if payload == "RELAY1_ON":
            GPIO.output(RELAY_PINS[0], GPIO.HIGH)
        elif payload == "RELAY1_OFF":
            GPIO.output(RELAY_PINS[0], GPIO.LOW)
        elif payload == "RELAY2_ON":
            GPIO.output(RELAY_PINS[1], GPIO.HIGH)
        elif payload == "RELAY2_OFF":
            GPIO.output(RELAY_PINS[1], GPIO.LOW)
        elif payload == "RELAY3_ON":
            GPIO.output(RELAY_PINS[2], GPIO.HIGH)
        elif payload == "RELAY3_OFF":
            GPIO.output(RELAY_PINS[2], GPIO.LOW)
        elif payload == "RELAY4_ON":
            GPIO.output(RELAY_PINS[3], GPIO.HIGH)
        elif payload == "RELAY4_OFF":
            GPIO.output(RELAY_PINS[3], GPIO.LOW)

       # self.reset_ptr_rx()
        #self.set_mode(MODE.RXSINGLE)

def main():
    receiver = LoRaReceiver(verbose=False)
    receiver.set_freq(868.0)
    receiver.set_pa_config(pa_select=1)
    receiver.set_bw(BW.BW125)
    receiver.set_coding_rate(CODING_RATE.CR4_5)
    receiver.set_spreading_factor(7)

    #receiver.set_mode(MODE.RXSINGLE)

    while True:
        time.sleep(2)
        receiver.on_rx_done()

    GPIO.cleanup()

if __name__ == '__main__':
    main()
