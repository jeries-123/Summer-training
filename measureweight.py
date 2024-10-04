import RPi.GPIO as GPIO
import time
from hx711 import HX711

# Set GPIO mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Initialize HX711 on GPIO pins
hx = HX711(dout_pin=9, pd_sck_pin=10)

# Placeholder for calibration factor (adjust during calibration)
calibration_factor = 102.372
zero_offset = 0

def tare_scale():
    global zero_offset
    try:
        print("Taring the scale... Please make sure it's empty and stable.")
        hx.reset()  # Reset the HX711

        # Take multiple readings for taring and calculate average
        raw_readings = [hx.get_raw_data_mean() for _ in range(20)]
        raw_readings = [value for value in raw_readings if value is not None]

        if len(raw_readings) == 0:
            raise ValueError("Failed to get valid readings during taring.")

        # Calculate zero offset and convert to integer
        zero_offset = int(sum(raw_readings) / len(raw_readings))
        hx.set_offset(zero_offset)  # Set the zero offset
        print(f"Taring complete. Zero offset: {zero_offset}")
    except Exception as e:
        print(f"Error during tare: {e}")

def calibrate_scale(known_weight_grams):
    try:
        # Set a trial calibration factor initially (any reasonable number)
        hx.set_scale_ratio(1)  # Set a temporary calibration ratio to get raw readings

        raw_value = hx.get_weight_mean(readings=10)
        if raw_value is None:
            raise ValueError("Failed to get valid data from HX711")

        # Calculate the calibration factor based on the known weight
        global calibration_factor
        calibration_factor = raw_value / known_weight_grams
        print(f"Calibration complete. Calibration factor: {calibration_factor}")

        # Set the calibration factor for subsequent readings
        hx.set_scale_ratio(calibration_factor)
    except Exception as e:
        print(f"Error during calibration: {e}")

def get_weight_filtered():
    try:
        # Get multiple readings and filter out outliers
        readings = [hx.get_weight_mean(readings=5) for _ in range(10)]
        readings = [value for value in readings if value is not None]

        if len(readings) < 5:
            raise ValueError("Not enough valid readings for filtering")

        # Sort readings and remove the top and bottom 10%
        readings.sort()
        filtered_readings = readings[len(readings) // 10: -len(readings) // 10]

        # Calculate the average of the filtered readings
        weight = sum(filtered_readings) / len(filtered_readings)
        weight_kg = weight / 1000  # Convert to kg

        # Print and return the weight
        print(f"Weight (filtered): {weight_kg:.2f} kg")
        return weight_kg
    except Exception as e:
        print(f"Error getting filtered weight: {e}")
        return None

if __name__ == '__main__':
    tare_scale()  # Tare the scale first
    calibrate_scale(1000)  # Use a known weight for calibration, e.g., 1000g
    while True:
        get_weight_filtered()  # Use the filtered version to get weight
        time.sleep(2)