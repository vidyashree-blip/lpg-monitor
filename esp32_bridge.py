import serial
import time
import requests

# Your Render website URL
SERVER_URL = "https://lpg-monitor-3ojt.onrender.com/api/sensor-data"

# ESP32 COM port
ESP32_PORT = "COM6"
BAUD_RATE  = 115200

def send_to_server(ppm, weight_kg):
    try:
        data = {
            "ppm": ppm,
            "weight_kg": weight_kg
        }
        response = requests.post(SERVER_URL, json=data)
        print(f"Server response: {response.status_code}")
    except Exception as e:
        print(f"Server error: {e}")

def read_esp32():
    print("Connecting to ESP32 on COM6...")
    try:
        ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)
        print("Connected! Reading data every 10 seconds...")

        while True:
            try:
                line = ser.readline().decode("utf-8").strip()
                if line:
                    print(f"ESP32 says: {line}")

                if "Gas Value:" in line:
                    gas_raw = float(line.split("Gas Value:")[1].strip())
                    ppm = round(gas_raw, 2)
                    weight_kg = 0.0

                    print(f"PPM: {ppm} | Weight: {weight_kg} kg")
                    send_to_server(ppm, weight_kg)

            except Exception as e:
                print(f"Read error: {e}")
                time.sleep(2)

            time.sleep(10)

    except Exception as e:
        print(f"Connection error: {e}")
        print("Make sure Arduino IDE is closed and ESP32 is connected!")

if __name__ == "__main__":
    read_esp32()