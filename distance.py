import RPi.GPIO as GPIO
import time

# GPIO pins
TRIG = 17
ECHO = 27

#treshold
TRESHOLD = 200

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

while True:
    GPIO.output(TRIG, False)
    time.sleep(2E-6)
    GPIO.output(TRIG, True)
    time.sleep(10E-6)
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
    print("Distance:",distance," cm")
    if distance <= TRESHOLD:
        print("Object Detected")
    time.sleep(1)

GPIO.cleanup()
