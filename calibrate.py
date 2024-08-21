import RPi.GPIO as GPIO
from hx711 import HX711

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize HX711
hx = HX711(dout_pin=9, pd_sck_pin=10)

# Tare the load cell (remove any weight)
hx.reset()
hx.zero()

# Save the tare offset
tare_offset = hx.get_current_offset()
print(f"Tare offset: {tare_offset}")

print("Place a known weight on the scale and press Enter")
input()

# Read raw value from HX711
raw_data = hx.get_data_mean()
if raw_data:
    print(f"Raw data: {raw_data}")
else:
    print("Error: Could not read from the HX711")

# Ask the user for the known weight
known_weight = float(input("Enter the weight (in grams) of the known mass: "))

# Calculate scale factor
calibration_factor = raw_data / known_weight
print(f"Calibration factor: {calibration_factor}")


GPIO.cleanup()
