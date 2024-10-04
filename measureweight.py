import RPi.GPIO as GPIO
import time
from hx711 import HX711

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

hx = HX711(dout_pin=9, pd_sck_pin=10)

calibration_factor = 102.372
zero_offset = 0

def tare_scale():
    global zero_offset
    try:
        print("Taring the scale... Please make sure it's empty and stable.")
        hx.reset()
        time.sleep(2)  # Allow some time for the sensor to stabilize

        raw_readings = []
        for _ in range(50):
            reading = hx.get_raw_data_mean()
            if reading is not None:
                raw_readings.append(reading)
            time.sleep(0.1)  # Add delay between readings to reduce noise

        if not raw_readings:
            raise ValueError("Failed to get valid readings during taring.")

        zero_offset = int(sum(raw_readings) / len(raw_readings))
        hx.set_offset(zero_offset)
        print(f"Taring complete. Zero offset: {zero_offset}")
    except Exception as e:
        print(f"Error during tare: {e}")

def calibrate_scale(known_weight_grams):
    try:
        hx.set_scale_ratio(1)
        time.sleep(2)  # Allow some time for the sensor to stabilize

        raw_value = hx.get_weight_mean(readings=20)
        if raw_value is None:
            raise ValueError("Failed to get valid data from HX711")

        global calibration_factor
        calibration_factor = abs(raw_value / known_weight_grams)
        print(f"Calibration complete. Calibration factor: {calibration_factor}")

        hx.set_scale_ratio(calibration_factor)
    except Exception as e:
        print(f"Error during calibration: {e}")

def get_weight_filtered():
    try:
        readings = []
        for _ in range(15):
            reading = hx.get_weight_mean(readings=10)
            if reading is not None:
                readings.append(reading)
            time.sleep(0.1)  # Add delay between readings to reduce noise

        if len(readings) < 10:
            raise ValueError("Not enough valid readings for filtering")

        readings.sort()
        filtered_readings = readings[len(readings) // 10: -len(readings) // 10]

        weight = sum(filtered_readings) / len(filtered_readings)
        weight_kg = weight / 1000

        print(f"Weight (filtered): {weight_kg:.2f} kg")
        return weight_kg
    except Exception as e:
        print(f"Error getting filtered weight: {e}")
        return None

if __name__ == '__main__':
    tare_scale()
    calibrate_scale(1000)
    while True:
        get_weight_filtered()
        time.sleep(2)