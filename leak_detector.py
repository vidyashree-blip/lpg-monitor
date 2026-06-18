from notifier import send_email_alert

SAFE_LEVEL    = 200
WARNING_LEVEL = 500
DANGER_LEVEL  = 1000

def detect_leak(ppm):
    if ppm >= DANGER_LEVEL:
        send_email_alert(
            "DANGER: Gas Leak Detected!",
            f"GAS LEAK! PPM: {ppm} - Evacuate immediately!"
        )
        return {
            "status": "DANGER",
            "message": f"GAS LEAK! PPM: {ppm} - Evacuate immediately!",
            "alert": True
        }

    elif ppm >= WARNING_LEVEL:
        send_email_alert(
            "WARNING: High Gas Level",
            f"High gas level! PPM: {ppm} - Check surroundings."
        )
        return {
            "status": "WARNING",
            "message": f"High gas level! PPM: {ppm} - Check surroundings.",
            "alert": True
        }

    else:
        return {
            "status": "SAFE",
            "message": f"Gas level normal. PPM: {ppm}",
            "alert": False
        }