import RPi.GPIO as GPIO
import time

#set GPIO pin for sound sensor
SOUND_PIN = 3

#set GPIO mode
GPIO.setmode(GPIO.BCM)

#set sound_pin as input
GPIO.setup(SOUND_PIN, GPIO.IN)

while True:
    #read digital input of sensor
    sound_detected = GPIO.input(SOUND_PIN)
        
    if sound_detected == 0:
        print("Sound Detected!")
    else:
        print("No Sound")            
    time.sleep(0.1)

GPIO.cleanup()
