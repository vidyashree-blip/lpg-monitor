import serial
import time
import random

def read_sensor_data(simulate=False):
    if simulate:
        ppm = random.randint(100, 1200)
        weight_kg = round(random.uniform(2.0, 14.2), 2)
        return {"ppm": ppm, "weight_kg": weight_kg}
    
    else:
        try:
            # Try to read from ESP32 via USB Serial
            ser = serial.Serial("COM3", 115200, timeout=2)
            time.sleep(2)
            
            line = ser.readline().decode("utf-8").strip()
            ser.close()
            
            print(f"Raw data from ESP32: {line}")
            
            # Parse "Gas Value: 1245"
            if "Gas Value:" in line:
                gas_value = float(line.split("Gas Value:")[1].strip())
                # Convert raw gas value to PPM
                ppm = (gas_value / 4095) * 1200
                
                return {
                    "ppm": round(ppm, 2),
                    "weight_kg": 0.0  # Add load cell later
                }
            
            return None
            
        except Exception as e:
            print(f"Sensor error: {e}")
            return None