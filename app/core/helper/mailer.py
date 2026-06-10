import os
from array import array
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydoc import html
from smtplib import SMTP
from dotenv import load_dotenv

load_dotenv()


class Mailer:
    def _send_mail(
        self, subject: str, to_email: array, body: html, from_add=None, cc_email=None
    ):
        message = MIMEMultipart()
        if not from_add:
            from_add = f"ExpenseFlow <{os.getenv('SMTP_SENDER')}>"
        message["Subject"] = subject
        message["From"] = from_add
        message["To"] = to_email
        if cc_email is not None:
            message["Cc"] = ", ".join(cc_email)
            cc = ", ".join(cc_email)
            to_email = to_email + ", " + cc
            to_email = to_email.split(",")
        message.attach(MIMEText(body, "html"))
        msgBody = message.as_string()

        server = SMTP(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT"))
        # server.starttls()
        # server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
        try:
            server.sendmail(from_add, to_email, msgBody)
            server.quit()
            return True
        except Exception as e:
            return False
