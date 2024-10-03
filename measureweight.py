from hx711 import HX711
import time

# Initialize HX711
hx = HX711(dout_pin=9, pd_sck_pin=10)

# Tare the scale
hx.reset()

# Try to get some raw data
for i in range(10):
    try:
        raw_data = hx.get_raw_data()
        print(f"Raw data: {raw_data}")
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
