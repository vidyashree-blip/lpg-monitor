import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your email settings
SENDER_EMAIL    = "your@gmail.com"      # Your Gmail
APP_PASSWORD    = "xxxx xxxx xxxx xxxx" # 16-digit app password
RECEIVER_EMAIL  = "your@gmail.com"      # Where alert goes (can be same)

def send_email_alert(subject, message):
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
        print("📧 Email alert sent!")
    except Exception as e:
        print(f"Email error: {e}")

def send_telegram_alert(message):
    # Routes to email instead
    if "LEAK" in message or "WARNING" in message:
        send_email_alert("🚨 LPG Gas Alert!", message)
    else:
        print(f"[LOG]: {message}")