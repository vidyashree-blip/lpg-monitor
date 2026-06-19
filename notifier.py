import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email settings
SENDER_EMAIL   = os.environ.get("SENDER_EMAIL")
APP_PASSWORD   = os.environ.get("APP_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

# Cooldown to avoid spam (5 minutes)
last_alert_time = 0
ALERT_COOLDOWN  = 300

def send_email_alert(subject, message):
    global last_alert_time

    current_time = time.time()
    if current_time - last_alert_time < ALERT_COOLDOWN:
        print("Cooldown active - email not sent")
        return

    try:
        msg = MIMEMultipart()
        msg["From"]    = SENDER_EMAIL
        msg["To"]      = RECEIVER_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        last_alert_time = current_time
        print("Email alert sent!")

    except Exception as e:
        print(f"Email error: {e}")