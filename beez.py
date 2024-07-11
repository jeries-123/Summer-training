import RPi.GPIO as GPIO
import adafruit_dht
import board
import time

# Initialize the DHT11 device, with data pin connected to GPIO2:
dht_device = adafruit_dht.DHT11(board.D2)
SOUND = 3
TRIG = 17
ECHO = 27
LIGHT = 4

treshold = 150

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND,GPIO.IN)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(LIGHT,GPIO.IN)

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
    distance = (pulse_duration*34300)/2 # Speed of sound = 34300 cm/s (divide by 2 for one-way distance)
    distance = round(distance,1)
    if distance <= treshold:
      print("Object detected at ",distance,"cm")
      
def temperature_humidity():
  try:
        # Print the values to the serial console
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Temp: {temperature}°C    Humidity: {humidity}%")
  except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
  

def is_bee_alive():
  sound_detected = GPIO.input(SOUND)
  if sound_detected == 0:
        print("The Bees Are Alive!!!")
  else:
        print("There might be some issues with the bees please check the Hive") 
  
def is_hive_open():
  if GPIO.input(LIGHT) == GPIO.HIGH:
        print("Someone Opened the bee hive please check!!")

while True:
  temperature_humidity()
  get_distance()
  is_bee_alive()
  is_hive_open()
  
  time.sleep(5)

GPIO.cleanup()



