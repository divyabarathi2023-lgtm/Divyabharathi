# email_alert.py
import yagmail

# Replace with your Gmail and app password
SENDER_EMAIL = "divyabarathi2023@gmail.com"
APP_PASSWORD = "your_app_password"  # Use Gmail App Password, not normal password
RECEIVER_EMAIL = "23cst012@vcew.ac.in"

def send_email(subject, body):
    yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
    yag.send(to=RECEIVER_EMAIL, subject=subject, contents=body)
    print("📧 Email sent successfully!")