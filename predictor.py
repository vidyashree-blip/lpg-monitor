import numpy as np
from database import get_last_7_days
from datetime import datetime, timedelta

def predict_runout():
    data = get_last_7_days()
    if len(data) < 3:
        return "⏳ Need at least 3 days of data to predict runout."

    base_time = datetime.fromisoformat(data[0][0])
    X, y = [], []
    for timestamp, weight in data:
        t = datetime.fromisoformat(timestamp)
        days = (t - base_time).total_seconds() / 86400
        X.append(days)
        y.append(weight)

    X = np.array(X)
    y = np.array(y)
    x_mean, y_mean = np.mean(X), np.mean(y)
    slope = np.sum((X - x_mean) * (y - y_mean)) / np.sum((X - x_mean) ** 2)
    intercept = y_mean - slope * x_mean

    if slope >= 0:
        return "⚠️ Cannot predict — usage pattern unclear."

    days_left = -intercept / slope
    runout_date = base_time + timedelta(days=days_left)
    return (
        f"🔮 Gas will run out in ~{int(days_left)} days\n"
        f"📅 Expected date: {runout_date.strftime('%d %B %Y')}"
    )