import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)
LIGHT_PIN = 4
GPIO.setup(LIGHT_PIN, GPIO.IN)

while True:
    if GPIO.input(LIGHT_PIN) == GPIO.HIGH:
        print("Light Detected")
    else:
        print("No Light Detected")
    time.sleep(1)
    
GPIO.cleanup()

