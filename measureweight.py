import RPi.GPIO as GPIO
import time
from hx711 import HX711

# Set GPIO pin numbering mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BCM

# Initialize HX711 on GPIO pins
hx = HX711(dout_pin=9, pd_sck_pin=10)

# Set calibration factor (adjust based on your load cell calibration)
calibration_factor = 102.372

def tare_scale():
    try:
        print("Taring the scale... Please make sure it's empty.")
        hx.reset()
        hx.set_reference_unit(calibration_factor)  # Set calibration factor
        hx.tare()  # Tare the scale
        print("Taring complete.")
    except Exception as e:
        print(f"Error during tare: {e}")

def get_weight():
    try:
        weight = hx.get_weight(5)  # Average over 5 readings
        weight_kg = weight / 1000  # Convert to kg
        print(f"Weight: {weight_kg:.2f} kg")
        return weight_kg
    except Exception as e:
        print(f"Error getting weight: {e}")
        return None

if __name__ == '__main__':
    tare_scale()  # Tare the scale
    while True:
        get_weight()  # Measure the weight
        time.sleep(2)
