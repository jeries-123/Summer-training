from flask import Flask, jsonify
import RPi.GPIO as GPIO
import adafruit_dht
import board
import time
import requests
import threading
from hx711 import HX711

app = Flask(__name__)

# Initialize the DHT11 device, with data pin connected to GPIO2:
dht_device = adafruit_dht.DHT11(board.D2)

# Define GPIO pins for other components
SOUND = 3
TRIG = 17
ECHO = 27
LIGHT = 4

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LIGHT, GPIO.IN)

# Initialize HX711 for weight measurement
hx = HX711(dout_pin=9, pd_sck_pin=10)

# Perform manual tare (zero the scale) by taking a reading with no weight on the sensor
hx.set_offset(hx.get_raw_data_mean(readings=100))  # Read the raw data and set it as the offset
print(f'Offset set for tare: {hx.offset}')

# Set the scale ratio for calibration
ratio = 102.372  # Calibration factor (depends on your load cell and setup)
hx.set_scale_ratio(ratio)
print(f'Scale ratio set to: {ratio}')

def get_distance():
    """Measure distance using the ultrasonic sensor."""
    GPIO.output(TRIG, False)
    time.sleep(0.000002)
    GPIO.output(TRIG, True)
    time.sleep(0.000001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        pass
    pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pass
    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Speed of sound = 34300 cm/s
    distance = round(distance, 1)
    return distance

def temperature_humidity():
    """Read temperature and humidity from the DHT11 sensor."""
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return {"temperature": temperature, "humidity": humidity}
    except RuntimeError as error:
        return {"error": error.args[0]}

def is_bee_alive():
    """Check if a bee is alive based on sound detection."""
    sound_detected = GPIO.input(SOUND)
    return sound_detected == 0

def is_hive_open():
    """Check if the hive is open based on the light sensor."""
    return GPIO.input(LIGHT) == GPIO.HIGH

def get_weight():
    """Get the current weight measurement from the HX711 sensor."""
    weight = hx.get_weight_mean(readings=5)  # Take the mean of 5 readings
    kgweight = weight / 1000  # Convert to kg
    hx.power_down()  # Power down the HX711 to save power
    hx.power_up()    # Power up the HX711 for the next reading
    return kgweight

def send_data():
    """Send sensor data to the remote API."""
    while True:
        data = {
            "temperature_humidity": temperature_humidity(),
            "distance": get_distance(),
            "bees_alive": is_bee_alive(),
            "hive_open": is_hive_open(),
            "weight": get_weight()  # Include weight data
        }
        
        # Send data to the remote API endpoint
        try:
            response = requests.post('http://bees.aiiot.center/api.php', json=data)
            if response.status_code == 200:
                print('Data sent successfully:', response.json())
            else:
                print('Failed to send data:', response.status_code, response.text)
        except Exception as e:
            print('Error sending data:', e)
        
        time.sleep(0.005)  # Sleep for 0.005 sec (you may want to increase this to reduce API calls)

@app.route('/data', methods=['GET'])
def get_data():
    """Provide sensor data via a GET API."""
    data = {
        "temperature_humidity": temperature_humidity(),
        "distance": get_distance(),
        "bees_alive": is_bee_alive(),
        "hive_open": is_hive_open(),
        "weight": get_weight()  # Include weight data in the API response
    }
    return jsonify(data)

if __name__ == '__main__':
    # Start a background thread to send data continuously
    data_thread = threading.Thread(target=send_data)
    data_thread.daemon = True  # This will allow the thread to exit when the main program exits
    data_thread.start()
    app.run(host='0.0.0.0', port=5000)
