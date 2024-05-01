import smtplib
import os

from email.message import EmailMessage
from constants import Env, Trade, Holding


class Mail:
    @staticmethod
    def send_email(subject, body):
        email_address = os.environ.get(Env.EMAIL_ADDRESS)
        password = os.environ.get(Env.EMAIL_PASSWORD)
        recipients = os.environ.get(Env.EMAIL_RECIPIENTS)

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = email_address
        msg["To"] = recipients
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_address, password)
            smtp.send_message(msg)

    @staticmethod
    def send_entry_email(entry_details):
        subject = f"Algo Trading - Entry Alert: {entry_details[Holding.SYMBOL]}"
        body = "\n".join([f"{key}: {value}" for key, value in entry_details.items()])
        Mail.send_email(subject, body)

    @staticmethod
    def send_exit_email(exit_details):
        subject = f"Algo Trading - Exit Alert: {exit_details[Trade.SYMBOL]}"
        body = "\n".join([f"{key}: {value}" for key, value in exit_details.items()])
        Mail.send_email(subject, body)

    @staticmethod
    def send_error_email(error):
        subject = "Algo Trading - Error Alert - Trading Stopped"
        body = error
        Mail.send_email(subject, body)

    @staticmethod
    def send_market_close_email(reason):
        subject = "Algo Trading - Market Closed"
        body = f"Market is closed due to: {reason}"
        Mail.send_email(subject, body)

    @staticmethod
    def send_trading_started_email():
        subject = "Algo Trading - Trading Started"
        body = "Trading has been started."
        Mail.send_email(subject, body)
