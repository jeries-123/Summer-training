from flask import Flask, jsonify
import RPi.GPIO as GPIO
import adafruit_dht
import board
import time
import requests
import threading
from hx711 import HX711

app = Flask(__name__)

# Initialize DHT11 (Temperature and Humidity sensor) on GPIO2
dht_device = adafruit_dht.DHT11(board.D2)

# Pin configuration
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

# Calibration factor for the load cell (adjust based on calibration)
calibration_factor = 102.372

# Function to tare (zero) the scale
def tare_scale():
    try:
        print("Taring the scale... Please make sure it's empty.")
        time.sleep(2)  # Allow some time for the scale to stabilize
        hx.reset()
        hx.set_scale_ratio(calibration_factor)
        print("Scale tared successfully.")
    except Exception as e:
        print(f"Error during tare: {e}")

# Function to get distance from the ultrasonic sensor
def get_distance():
    try:
        GPIO.output(TRIG, False)
        time.sleep(0.000002)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pass
        pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pass
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 34300) / 2  # cm
        return round(distance, 1)
    except Exception as e:
        print(f"Error getting distance: {e}")
        return None

# Function to read temperature and humidity from DHT11
def temperature_humidity():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return {"temperature": temperature, "humidity": humidity}
    except RuntimeError as error:
        print(f"Error reading DHT11: {error}")
        return {"error": str(error)}

# Function to check if bees are alive using the sound sensor
def is_bee_alive():
    try:
        return GPIO.input(SOUND) == 0
    except Exception as e:
        print(f"Error checking bee sound sensor: {e}")
        return None

# Function to check if hive is open using the light sensor
def is_hive_open():
    try:
        return GPIO.input(LIGHT) == GPIO.HIGH
    except Exception as e:
        print(f"Error checking hive light sensor: {e}")
        return None

# Function to get weight measurement from HX711
def get_weight():
    try:
        weight = hx.get_weight_mean(readings=5)  # Average of 5 readings
        return weight / 1000  # Convert to kg
    except Exception as e:
        print(f"Error getting weight: {e}")
        return None

# Function to send data to remote API endpoint
def send_data():
    while True:
        data = {
            "temperature_humidity": temperature_humidity(),
            "distance": get_distance(),
            "bees_alive": is_bee_alive(),
            "hive_open": is_hive_open(),
            "weight": get_weight()
        }

        try:
            response = requests.post('http://bees.aiiot.center/api.php', json=data)
            if response.status_code == 200:
                print('Data sent successfully:', response.json())
            else:
                print(f'Failed to send data: {response.status_code} - {response.text}')
        except Exception as e:
            print(f'Error sending data: {e}')
        
        time.sleep(5)  # Wait 5 seconds before sending the next set of data

# Flask route to fetch sensor data as JSON
@app.route('/data', methods=['GET'])
def get_data():
    data = {
        "temperature_humidity": temperature_humidity(),
        "distance": get_distance(),
        "bees_alive": is_bee_alive(),
        "hive_open": is_hive_open(),
        "weight": get_weight()
    }
    return jsonify(data)

# Main function to run the Flask server and tare the scale
if __name__ == '__main__':
    tare_scale()  # Tare the scale on startup
    data_thread = threading.Thread(target=send_data)
    data_thread.daemon = True  # Set thread as daemon to close with main program
    data_thread.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000)

    # Clean up GPIO pins on exit
    GPIO.cleanup()
