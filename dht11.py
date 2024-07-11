import time
import board
import adafruit_dht

# Initialize the DHT11 device, with data pin connected to GPIO2:
dht_device = adafruit_dht.DHT11(board.D2)

while True:
    try:
        # Print the values to the serial console
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Temp: {temperature}°C    Humidity: {humidity}%")
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
    time.sleep(2.0)
