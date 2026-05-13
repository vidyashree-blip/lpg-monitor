SAFE_LEVEL = 200
WARNING_LEVEL = 500
DANGER_LEVEL = 1000

def detect_leak(ppm):
    if ppm >= DANGER_LEVEL:
        return {
            "status": "DANGER",
            "message": f"🚨 GAS LEAK! PPM: {ppm} — Evacuate immediately!",
            "alert": True
        }
    elif ppm >= WARNING_LEVEL:
        return {
            "status": "WARNING",
            "message": f"⚠️ High gas level! PPM: {ppm} — Check surroundings.",
            "alert": True
        }
    else:
        return {
            "status": "SAFE",
            "message": f"✅ Gas level normal. PPM: {ppm}",
            "alert": False
        }