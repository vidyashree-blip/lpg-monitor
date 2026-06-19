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
        return {
            "status": "DANGER",
            "message": f"GAS LEAK! PPM: {ppm} - Evacuate immediately!",
            "alert": True
        }
    elif ppm >= WARNING_LEVEL:
        return {
            "status": "WARNING",
            "message": f"High gas level! PPM: {ppm}",
            "alert": True
        }
    else:
        return {
            "status": "SAFE",
            "message": f"Gas level normal. PPM: {ppm}",
            "alert": False
        }