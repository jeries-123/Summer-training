import RPi.GPIO as GPIO
from hx711 import HX711
import time

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize HX711
hx = HX711(dout_pin=9, pd_sck_pin=10)

# Set the calibration factor and tare offset
#you have to put into consideration that the tare_offset and calibration_factor 
#might change due to a platform placed on the weight sensor before weighing. 
#if there is a platform, first go to the calibration program and run it first to have a new calibration_factor and tare_offset. 
#this is with platform
calibration_factor = 102.372
tare_offset = 159054  

hx.set_scale_ratio(calibration_factor)
hx.set_offset(tare_offset)

print("Ready to measure. Place items on the scale to weigh.")

# Measure weight continuously
try:
    while True:
        weight = hx.get_weight_mean(20)
        print(f"Weight: {weight:.2f} grams")
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped.")
finally:
    GPIO.cleanup()

