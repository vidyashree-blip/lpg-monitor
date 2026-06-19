SAFE_LEVEL    = 200
WARNING_LEVEL = 400
DANGER_LEVEL  = 550

def detect_leak(ppm):
    try:
        from notifier import send_email_alert
        if ppm >= DANGER_LEVEL:
            send_email_alert(
                "DANGER: Gas Leak Detected!",
                f"GAS LEAK! PPM: {ppm} - Evacuate immediately!"
            )
    except Exception as e:
        print(f"Email error: {e}")

    if ppm >= DANGER_LEVEL:
        return {"status": "DANGER", "alert": True}
    elif ppm >= WARNING_LEVEL:
        return {"status": "WARNING", "alert": True}
    else:
        return {"status": "SAFE", "alert": False}