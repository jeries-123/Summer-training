import RPi.GPIO as GPIO
import time
from hx711 import HX711

# Set GPIO mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Initialize HX711 on GPIO pins
hx = HX711(dout_pin=9, pd_sck_pin=10)

# Calibration factor (adjust based on your load cell calibration)
calibration_factor = 102.372
zero_offset = 0

def tare_scale():
    global zero_offset
    try:
        print("Taring the scale... Please make sure it's empty.")
        hx.reset()  # Reset the HX711

        # Get average raw reading as the zero offset
        zero_offset = hx.get_raw_data_mean(readings=10)
        if zero_offset is None:
            raise ValueError("Failed to get valid readings during taring.")

        hx.set_offset(zero_offset)  # Set the zero offset
        print(f"Taring complete. Zero offset: {zero_offset}")
    except Exception as e:
        print(f"Error during tare: {e}")

def get_weight():
    try:
        # Set the calibration factor for weight calculation
        hx.set_scale_ratio(calibration_factor)
        
        # Get the mean weight based on multiple readings
        weight = hx.get_weight_mean(readings=5)  # Get average weight over 5 readings
        if weight is None:
            raise ValueError("Failed to get data from HX711")

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
