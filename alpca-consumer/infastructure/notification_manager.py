import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:

    @staticmethod
    def send_email(stock, subject: str = None, body: str = None):
        # Set up the email server and the message
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = "omerahmed41@gmail.com"
        receiver_email = "xzoneappledeveloper@gmail.com"
        password = os.getenv('GMAIL_APP_PASSWORD')
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        if not subject:
            subject = f"Trading alert: {stock}"
        message["Subject"] = subject

        # Add body to email
        if not body:
            body = f"Buy {stock}"

        message.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP(smtp_server, port)

        try:
            # Connect to the server and send the email
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()

