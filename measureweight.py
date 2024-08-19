import RPi.GPIO as GPIO
from hx711 import HX711
import time

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize HX711
hx = HX711(dout_pin=9, pd_sck_pin=10)

# Set the calibration factor and tare offset
calibration_factor = 106.582
tare_offset = 45422

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

