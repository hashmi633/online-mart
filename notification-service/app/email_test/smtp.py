import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.settings import EMAIL, PASSWORD

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = EMAIL
EMAIL_PASSWORD = PASSWORD

async def to_send_email(to_email, subject, body):
    try:
        # Set up the MIME
        message = MIMEMultipart()
        message["From"] = EMAIL_USERNAME
        message["To"] = to_email
        message["Subject"] = subject

        # Email body
        message.attach(MIMEText(body, "plain"))

        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(message)
        print(f"Email sent successfully to {to_email}")
        return {"Email sent successfully"}

    except Exception as e:
        print(f"Failed to send email: {e}")
        return {"Failed to send email"}
    
# Test the function
# send_email(
#     to_email="faizahashmi50@gmail.com",  # Use your own email for testing
#     subject="Order Created - Pending",
#     body="Your order has been successfully created and is currently pending. Thank you!"
# )

