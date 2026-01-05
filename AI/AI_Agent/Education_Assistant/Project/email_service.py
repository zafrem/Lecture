import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configuration (In production, use environment variables)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "teacher_agent@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "fake_password")

def send_email(to_address, subject, body):
    """
    Sends an email to a single recipient.
    If credentials are valid, it sends real email.
    Otherwise, it prints a mock log (useful for testing).
    """
    if EMAIL_PASSWORD == "fake_password":
        print(f"\n[Email Service MOCK] 📧 Sending to {to_address}")
        print(f"   Subject: {subject}")
        print(f"   Body: {body[:50]}...") 
        return True

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[Email Service] ✅ Sent to {to_address}")
        return True
    except Exception as e:
        print(f"[Email Service] ❌ Failed to send to {to_address}: {e}")
        return False
