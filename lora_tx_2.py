import time
from SX127x.LoRa import *
import RPi.GPIO as GPIO

# GPIO pin mapping
DIO0 = 16

class LoRaSender(LoRa):
    def __init__(self, verbose=False):
        #super(LoRaSender, self).__init__(verbose)
        self.setup_gpio()
        self.set_mode(MODE.STDBY)
        
        
        self.set_dio_mapping([1,0,0,0,0,0])
        

    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(DIO0, GPIO.IN)

    def send_message(self, message):
        self.set_mode(MODE.STDBY)
        self.write_payload(list(message))  # Convert message to a list
        self.set_mode(MODE.TX)
        # Wait for transmission to complete or timeout after 5 seconds
        time.sleep(100)  # Wait for 5 seconds
        #self.set_mode(MODE.STDBY)

def main():
    sender = LoRaSender(verbose=False)
    sender.set_freq(868.0)
    sender.set_pa_config(pa_select=1)
    sender.set_bw(BW.BW125)
    sender.set_coding_rate(CODING_RATE.CR4_5)
    sender.set_spreading_factor(7)

    message = input("Enter message to send: ")
    print(message.encode())
    sender.send_message(message.encode())

    GPIO.cleanup()

if __name__ == '__main__':
    main()
