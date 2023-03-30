import smtplib
from email.message import EmailMessage
from ..config.config import EMAIL_SERVICE
from typing import cast

def send_email(subject: str, email_content: str) -> None:

    _email = EmailMessage()
    _email['From'] = EMAIL_SERVICE.FROM
    _email['Subject'] = subject
    _email['To'] = EMAIL_SERVICE.TO
    _email.set_content(email_content)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(cast(str, EMAIL_SERVICE.FROM ), 'vbtlrggzgqbitzwy')
        smtp.send_message(_email)