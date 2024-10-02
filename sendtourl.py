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

# Set the calibration factor and tare offset
calibration_factor = 102.372  # Adjust this based on your calibration
hx.set_scale_ratio(calibration_factor)
print(f'Scale ratio set to: {calibration_factor}')

# Tare the scale to set the current weight to zero
def tare_scale():
    print("Taring the scale... Please make sure it's empty.")
    time.sleep(2)  # Allow some time for the scale to stabilize
    hx.reset()  # Reset the HX711
    print("Scale tared.")

# Function to get distance from the ultrasonic sensor
def get_distance():
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
    distance = (pulse_duration * 34300) / 2  # Speed of sound = 34300 cm/s (divide by 2 for one-way distance)
    return round(distance, 1)

# Function to read temperature and humidity
def temperature_humidity():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return {"temperature": temperature, "humidity": humidity}
    except RuntimeError as error:
        return {"error": error.args[0]}

# Function to check if the hive is open or if bees are alive
def is_bee_alive():
    sound_detected = GPIO.input(SOUND)
    return sound_detected == 0

def is_hive_open():
    return GPIO.input(LIGHT) == GPIO.HIGH

# Function to get weight measurement
def get_weight():
    weight = hx.get_weight_mean(readings=5)  # Get the mean of 5 readings
    kg_weight = weight / 1000  # Convert to kg
    return kg_weight

# Function to send data to the remote API endpoint
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
                print('Failed to send data:', response.status_code, response.text)
        except Exception as e:
            print('Error sending data:', e)

        time.sleep(0.005)  # Sleep for 5 milliseconds

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

if __name__ == '__main__':
    tare_scale()  # Call tare scale on startup
    data_thread = threading.Thread(target=send_data)
    data_thread.daemon = True  # This will allow the thread to exit when the main program exits
    data_thread.start()
    app.run(host='0.0.0.0', port=5000)

    GPIO.cleanup()  # Reset GPIO pins on exit
