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

reading = hx.get_data_mean(readings=100)

# Set the calibration factor and tare offset

#you have to put into consideration that the tare_offset and calibration_factor 
#might change due to a platform placed on the weight sensor before weighing. 
#if there is a platform, first go to the calibration program and run it first to have a new calibration_factor and tare_offset. 
#this is with platform
tare_offset = 159054
hx.set_offset(tare_offset)
print(f'Tare offset set to: {tare_offset}')

ratio = 102.372
hx.set_scale_ratio(ratio)
print(f'Scale ratio set to: {ratio}')

def get_distance():
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
    distance = (pulse_duration * 34300) / 2  # Speed of sound = 34300 cm/s (divide by 2 for one-way distance)
    distance = round(distance, 1)
    return distance

def temperature_humidity():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return {"temperature": temperature, "humidity": humidity}
    except RuntimeError as error:
        return {"error": error.args[0]}

def is_bee_alive():
    sound_detected = GPIO.input(SOUND)
    return sound_detected == 0

def is_hive_open():
    return GPIO.input(LIGHT) == GPIO.HIGH

def get_weight():
    # Get the current weight measurement
    weight = hx.get_weight_mean(readings=5) # Take the mean of 5 readings	
    kgweight = weight/1000 #convert to kg
    return kgweight

def send_data():
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
            response = requests.post('http://profdux.education/api.php', json=data)
            if response.status_code == 200:
                print('Data sent successfully:', response.json())
            else:
                print('Failed to send data:', response.status_code, response.text)
        except Exception as e:
            print('Error sending data:', e)
        
        time.sleep(0.005)  # Sleep for 0.005 sec

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        "temperature_humidity": temperature_humidity(),
        "distance": get_distance(),
        "bees_alive": is_bee_alive(),
        "hive_open": is_hive_open(),
        "weight": get_weight()  # Include weight data in the API response
    }
    return jsonify(data)
    
if __name__ == '__main__':
    data_thread = threading.Thread(target=send_data)
    data_thread.daemon = True  # This will allow the thread to exit when the main program exits
    data_thread.start()
    app.run(host='0.0.0.0', port=5000)
