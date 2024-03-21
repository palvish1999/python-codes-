import Adafruit_DHT
import time
from azure.iot.device import IoTHubDeviceClient, Message

# We are using pin number 4 and the DHT22 sensor
sensor = Adafruit_DHT.DHT22
pin = 4  # This is GPIO pin number

# Define the connection string (replace with your actual connection string)
CONNECTION_STRING = "HostName=MabzonePiHub.azure-devices.net;DeviceId=MabzonePi123;SharedAccessKey=iyxjEpmSZwiGPPRDKVqTShKPfXe6cMnPxAIoTL66EEw="

# This is the array that will be used to store the data
MSG_SND = '{{"temperature": {temperature},"humidity": {humidity}}}'

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("AronAyub Pi is Sending data to IoT Hub. To exit, press Ctrl-C ")

        while True:
            # Read data from the DHT22 sensor
            humidity, temperature = 12,56
            print("Humidity :", humidity)
            print("Temperature :", temperature)

            if humidity is not None and temperature is not None:
                msg_txt_formatted = MSG_SND.format(temperature=temperature, humidity=humidity)
                message = Message(msg_txt_formatted)
                print("Sending message: {}".format(message))
                client.send_message(message)
                print("Message successfully sent")
            else:
                print("Failed to get reading. Try again!")

            time.sleep(5)

    except KeyboardInterrupt:
        print("IoTHubClient stopped")

if __name__ == '__main__':
    print("Press Ctrl-C to exit")
    iothub_client_telemetry_sample_run()

    iothub_client_telemetry_sample_run()
