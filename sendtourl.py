from flask import Flask, jsonify
import RPi.GPIO as GPIO
import adafruit_dht
import board
import time
import requests
import threading

app = Flask(__name__)

# Initialize the DHT11 device, with data pin connected to GPIO2
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

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.000002)  # Wait for 2 microseconds
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # Send a 10-microsecond pulse
    GPIO.output(TRIG, False)
    
    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Speed of sound = 34300 cm/s
    return round(distance, 1)

def temperature_humidity():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return {"temperature": temperature, "humidity": humidity}
    except RuntimeError as error:
        return {"error": str(error)}

def is_bee_alive():
    sound_detected = GPIO.input(SOUND)
    return sound_detected == 0  # Assuming LOW signal means a bee is present

def is_hive_open():
    return GPIO.input(LIGHT) == GPIO.HIGH  # Assuming HIGH signal means hive is open

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        "temperature_humidity": temperature_humidity(),
        "distance": get_distance(),
        "bees_alive": is_bee_alive(),
        "hive_open": is_hive_open(),
    }
    return jsonify(data)

def send_data():
    while True:
        data = {
            "temperature_humidity": temperature_humidity(),
            "distance": get_distance(),
            "bees_alive": is_bee_alive(),
            "hive_open": is_hive_open(),
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
        
        time.sleep(5)  # Sleep for 5 seconds before sending data again

if __name__ == '__main__':
    data_thread = threading.Thread(target=send_data)
    data_thread.daemon = True  # Allow thread to exit when the main program exits
    data_thread.start()
    app.run(host='0.0.0.0', port=5000)
