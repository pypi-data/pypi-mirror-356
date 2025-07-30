# darktrace_locks/email_handler.py
from dotenv import load_dotenv
load_dotenv()
import os
import smtplib
from email.message import EmailMessage

def send_otp_email(to_email, otp):
    try:
        app_password = os.environ.get("GMAIL_APP_PASSWORD")
        if not app_password:
            print("❌ Gmail app password not found in environment variables.")
            return

        msg = EmailMessage()
        msg.set_content(f"Your DARKTRACE OTP is: {otp}")
        msg['Subject'] = "DARKTRACE OTP Verification"
        msg['From'] = "Your Security System"
        msg['To'] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("anonymous@gmail.com", app_password)  # Gmail ID will be hidden
            smtp.send_message(msg)

        print("📧 OTP sent successfully (Gmail ID hidden).")

    except Exception as e:
        print("⚠️ Error sending OTP:", e)
