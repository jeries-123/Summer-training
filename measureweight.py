import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setwarnings(False)
hx = HX711(dout_pin=9, pd_sck_pin=10)

def tare_scale():
    print("Taring the scale... Please make sure it's empty.")
    hx.reset()
    hx.tare()
    print("Taring complete.")

def get_weight():
    try:
        weight = hx.get_weight(5)  # Average of 5 readings
        print(f"Weight: {weight / 1000} kg")  # Convert to kg and print
        return weight
    except Exception as e:
        print(f"Error getting weight: {e}")
        return None

if __name__ == '__main__':
    tare_scale()
    while True:
        weight = get_weight()
        time.sleep(2)
