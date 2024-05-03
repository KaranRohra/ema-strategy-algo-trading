import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from constants import Env, Trade, Holding, DATETIME_FORMAT
from mail import html_template
from datetime import datetime as dt


class Mail:
    @staticmethod
    def send_email(subject, body, body_content_type="plain"):
        email_address = os.environ.get(Env.EMAIL_ADDRESS)
        password = os.environ.get(Env.EMAIL_PASSWORD)
        recipients = os.environ.get(Env.EMAIL_RECIPIENTS)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject + " - " + dt.now().strftime("%d %b %Y")
        msg["From"] = email_address
        msg["To"] = recipients
        msg.attach(MIMEText(body, body_content_type))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_address, password)
            smtp.send_message(msg)

    @staticmethod
    def send_entry_email(entry_details):
        subject = f"Algo Trading - Entry Alert: {entry_details[Holding.SYMBOL]}"
        entry_details[Holding.DATETIME] = entry_details[Holding.DATETIME].strftime(
            DATETIME_FORMAT
        )
        Mail.send_email(
            subject,
            html_template.table_with_two_columns(entry_details),
            "html",
        )

    @staticmethod
    def send_exit_email(exit_details):
        subject = f"Algo Trading - Exit Alert: {exit_details[Trade.SYMBOL]}"
        exit_details[Trade.FROM] = exit_details[Trade.FROM].strftime(DATETIME_FORMAT)
        exit_details[Trade.TO] = exit_details[Trade.TO].strftime(DATETIME_FORMAT)
        Mail.send_email(
            subject,
            html_template.table_with_two_columns(exit_details),
            "html",
        )

    @staticmethod
    def send_error_email(error):
        subject = "Algo Trading - Error Alert - Trading Stopped"
        body = error
        Mail.send_email(subject, body)

    @staticmethod
    def send_market_close_email(reason):
        subject = "Algo Trading - Market Closed"
        body = f"Market is closed due to:\n{reason}"
        Mail.send_email(subject, body)

    @staticmethod
    def send_trading_started_email():
        subject = f"Algo Trading - Trading Started - {os.environ.get(Env.SYMBOL)}"
        body = "Trading is started."
        Mail.send_email(subject, body)
