
import random

def read_sensor_data(simulate=True):
    if simulate:
        ppm = random.randint(100, 1200)
        weight_kg = round(random.uniform(2.0, 14.2), 2)
        return {"ppm": ppm, "weight_kg": weight_kg}
    else:
        import serial
        import time
        try:
            ser = serial.Serial("COM3", 9600, timeout=1)
            time.sleep(2)
            line = ser.readline().decode("utf-8").strip()
            parts = dict(item.split(":") for item in line.split(","))
            return {
                "ppm": float(parts["PPM"]),
                "weight_kg": float(parts["WEIGHT"])
            }
        except Exception as e:
            print(f"Sensor error: {e}")
            return None