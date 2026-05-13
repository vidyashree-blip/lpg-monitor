import time
import schedule
from sensor_reader import read_sensor_data
from leak_detector import detect_leak
from database import init_db, save_reading
from notifier import send_telegram_alert
from usage_tracker import daily_usage_report
from predictor import predict_runout

def monitor_loop():
    data = read_sensor_data(simulate=True)
    if not data:
        return
    ppm = data["ppm"]
    weight = data["weight_kg"]
    result = detect_leak(ppm)
    print(result["message"])
    save_reading(ppm, weight, result["status"])
    if result["alert"]:
        send_telegram_alert(result["message"])

def send_daily_report():
    report = daily_usage_report()
    prediction = predict_runout()
    full_msg = report + "\n\n" + prediction
    print("\n" + "="*40)
    print(full_msg)
    print("="*40 + "\n")
    send_telegram_alert(full_msg)

schedule.every(10).seconds.do(monitor_loop)
schedule.every().day.at("08:00").do(send_daily_report)

if __name__ == "__main__":
    init_db()
    print("🔥 LPG Monitor Started! Press Ctrl+C to stop.\n")
    while True:
        schedule.run_pending()
        time.sleep(1)