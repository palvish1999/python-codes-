from machine import Pin
import time

# setup relay pin as output
relay = Pin(16, Pin.OUT)

while True:
    # turn on relay
    relay.value(1)
    #print relay state
    print("Relay On")
    time.sleep(5)
    # turn off relay
    relay.value(0)
    #print relay state
    print("Relay Off")
    time.sleep(5)