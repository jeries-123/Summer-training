# app.py

import os
import time
import logging
import threading
from typing import Dict, Union

import RPi.GPIO as GPIO
import adafruit_dht
import board
import requests
from flask import Flask, jsonify
from hx711 import HX711

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask app setup
app = Flask(__name__)

# Load environment variables for configuration
API_URL = os.getenv("API_URL", "http://profdux.education/api.php")
DHT_PIN = board.D2
SOUND_PIN = 3
TRIG_PIN = 17
ECHO_PIN = 27
LIGHT_PIN = 4
HX_DOUT_PIN = 9
HX_SCK_PIN = 10
COLLECTION_INTERVAL = float(os.getenv("COLLECTION_INTERVAL", 1.0))  # 1 second default

# Initialize GPIO and sensors
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup([SOUND_PIN, LIGHT_PIN], GPIO.IN)
GPIO.setup([TRIG_PIN], GPIO.OUT)
GPIO.setup([ECHO_PIN], GPIO.IN)

# Sensor instances
dht_device = adafruit_dht.DHT11(DHT_PIN)
hx = HX711(dout_pin=HX_DOUT_PIN, pd_sck_pin=HX_SCK_PIN)

# Sensor calibration
tare_offset = 159054
hx.set_offset(tare_offset)
hx.set_scale_ratio(102.372)

def get_distance() -> float:
    """Measure the distance using the ultrasonic sensor."""
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.000002)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.000001)
    GPIO.output(TRIG_PIN, False)

    pulse_start, pulse_end = time.time(), time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2
    return round(distance, 1)

def get_temperature_humidity() -> Dict[str, Union[float, str]]:
    """Get temperature and humidity readings from the DHT11 sensor."""
    try:
        return {"temperature": dht_device.temperature, "humidity": dht_device.humidity}
    except RuntimeError as error:
        logging.warning(f"DHT11 sensor error: {error}")
        return {"error": "Failed to read temperature/humidity"}

def is_bee_alive() -> bool:
    """Detect bee presence based on sound."""
    return GPIO.input(SOUND_PIN) == 0

def is_hive_open() -> bool:
    """Check if the hive is open based on light levels."""
    return GPIO.input(LIGHT_PIN) == GPIO.HIGH

def get_weight() -> float:
    """Retrieve weight from HX711 sensor."""
    weight = hx.get_weight_mean(readings=5)
    return weight / 1000  # Convert to kg

def send_data():
    """Send collected sensor data to a remote API at regular intervals."""
    while True:
        data = {
            "temperature_humidity": get_temperature_humidity(),
            "distance": get_distance(),
            "bees_alive": is_bee_alive(),
            "hive_open": is_hive_open(),
            "weight": get_weight()
        }

        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                logging.info("Data sent successfully.")
            else:
                logging.error(f"Failed to send data. Status code: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            logging.error(f"Error sending data: {e}")

        time.sleep(COLLECTION_INTERVAL)

@app.route('/data', methods=['GET'])
def get_data():
    """Flask endpoint to retrieve current sensor data."""
    data = {
        "temperature_humidity": get_temperature_humidity(),
        "distance": get_distance(),
        "bees_alive": is_bee_alive(),
        "hive_open": is_hive_open(),
        "weight": get_weight()
    }
    return jsonify(data)

if __name__ == '__main__':
    data_thread = threading.Thread(target=send_data)
    data_thread.daemon = True
    data_thread.start()
    app.run(host='0.0.0.0', port=5000)
