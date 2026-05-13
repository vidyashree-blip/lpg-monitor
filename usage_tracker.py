from database import get_today_readings
from datetime import datetime

def daily_usage_report():
    result = get_today_readings()
    today = datetime.now().date().isoformat()
    if result and result[0] and result[1]:
        used = round(result[0] - result[1], 3)
        remaining = result[1]
        return (
            f"📊 Daily Report — {today}\n"
            f"Used today  : {used} kg\n"
            f"Remaining   : {remaining} kg"
        )
    return f"📊 Daily Report — {today}\nNo data recorded yet."