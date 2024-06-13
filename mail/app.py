import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from constants import Env
from datetime import datetime as dt
from mail import html_template as ht


def send_email(subject, body, body_content_type="plain"):
    if os.environ.get(Env.SEND_EMAIL) == "0":
        return
    email_address = os.environ.get(Env.EMAIL_ADDRESS)
    password = os.environ.get(Env.EMAIL_PASSWORD)
    recipients = os.environ.get(Env.EMAIL_RECIPIENTS)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject + " - " + dt.now().strftime("%d %b %Y, %I:%M:%S %p")
    msg["From"] = email_address
    msg["To"] = recipients
    msg.attach(MIMEText(body, body_content_type))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_address, password)
        smtp.send_message(msg)


def send_error_email(error):
    subject = "Algo Trading - Error Alert"
    body = error
    send_email(subject, body)


def send_trading_stop_email():
    subject = "Algo Trading - Trading Stopped"
    body = "Trading is stopped."
    send_email(subject, body)


def send_trading_started_email(args):
    subject = f"Algo Trading - Trading Started"
    body = ht.multiple_table(args)
    send_email(subject, body, "html")
