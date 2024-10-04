from hx711 import HX711

hx = HX711(dout_pin=9, pd_sck_pin=10)

def tare_scale():
    try:
        print("Taring the scale... Please make sure it's empty.")
        hx.reset()  # Reset the HX711
        hx.tare()  # Tare the scale
        print("Scale tared successfully.")
    except Exception as e:
        print(f"Error during tare: {e}")

def get_weight():
    try:
        weight = hx.get_weight(5)  # Average of 5 readings
        return weight / 1000  # Convert to kg
    except Exception as e:
        print(f"Error getting weight: {e}")
        return None
