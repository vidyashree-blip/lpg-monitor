import serial
import time
import requests

SERVER_URL = "https://lpg-monitor-3ojt.onrender.com/api/sensor-data"
ESP32_PORT = "COM6"
BAUD_RATE  = 115200

def send_to_server(ppm, weight_kg):
    try:
        response = requests.post(SERVER_URL, json={
            "ppm": ppm,
            "weight_kg": weight_kg
        }, timeout=10)
        print(f"Server response: {response.status_code}")
    except Exception as e:
        print(f"Server error: {e}")

def read_esp32():
    print("Connecting to ESP32 on COM6...")
    try:
        ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)
        print("Connected! Reading data...")

        while True:
            try:
                line = ser.readline().decode("utf-8").strip()
                if line:
                    print(f"ESP32: {line}")
                if "Gas Value:" in line:
                    gas_raw = float(line.split("Gas Value:")[1].strip())
                    ppm = round(gas_raw, 2)
                    print(f"PPM: {ppm}")
                    send_to_server(ppm, 0.0)
            except Exception as e:
                print(f"Read error: {e}")
            time.sleep(10)

    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    read_esp32()