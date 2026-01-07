import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_SENDER = "pandeymridula23@gmail.com"
EMAIL_PASSWORD = "gapy itiw uesv curs"
BACKEND_URL = "http://localhost:8000"

async def send_set_password_email(to_email: str, token: str):
    reset_link = f"{BACKEND_URL}/auth/set-password?token={token}"

    message = EmailMessage()
    message["Subject"] = "Set your password"
    message["From"] = EMAIL_SENDER
    message["To"] = to_email

    message.set_content(f"""Hello,Welcome! Please click the link below to set your password:{reset_link}
This link will expire in 30 minutes.If you did not request this, please ignore this email.
Thanks,
Your Team""")
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(message)
    except Exception as e:
        print("Email sending failed:", e)
