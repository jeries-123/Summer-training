import RPi.GPIO as GPIO
import time
from hx711 import HX711

GPIO.setwarnings(False)

# Initialize HX711 on the appropriate GPIO pins
hx = HX711(dout_pin=9, pd_sck_pin=10)

# Global variable for zero offset
zero_offset = 0

def tare_scale():
    global zero_offset
    try:
        print("Taring the scale... Please make sure it's empty.")
        hx.reset()  # Reset HX711 to its initial state

        # Take multiple raw readings and average them to determine the zero offset
        raw_readings = []
        for _ in range(10):
            raw_value = hx.read()  # Use read() or equivalent method to get raw value
            if raw_value is not None:
                raw_readings.append(raw_value)
            time.sleep(0.1)

        if raw_readings:
            zero_offset = sum(raw_readings) / len(raw_readings)
            print(f"Taring complete. Zero offset: {zero_offset}")
        else:
            raise ValueError("Failed to get valid readings during taring.")
    except Exception as e:
        print(f"Error during tare: {e}")

def get_weight():
    try:
        raw_value = hx.read()  # Read raw value from HX711
        if raw_value is None:
            raise ValueError("Failed to get data from HX711")

        # Subtract zero offset and divide by calibration factor to get weight
        weight = (raw_value - zero_offset) / 102.372  # Adjust calibration factor accordingly
        weight_kg = weight / 1000  # Convert to kg
        print(f"Weight: {weight_kg:.2f} kg")
        return weight_kg
    except Exception as e:
        print(f"Error getting weight: {e}")
        return None

if __name__ == '__main__':
    tare_scale()  # Tare the scale before taking measurements
    while True:
        get_weight()  # Measure the weight continuously
        time.sleep(2)
