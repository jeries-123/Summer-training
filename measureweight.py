import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Initialize HX711 on GPIO pins
hx = HX711(dout_pin=9, pd_sck_pin=10)

# Print available methods and attributes of HX711 object
print(dir(hx))
