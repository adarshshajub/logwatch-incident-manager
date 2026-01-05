import smtplib
from email.message import EmailMessage
from flask import current_app


def send_email(to, subject, body, html_content=None, importance="normal"):
    msg = EmailMessage()
    msg["From"] = current_app.MAIL_USERNAME
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject

    importance_map = {
        "high": ("High", "1"),
        "normal": ("Normal", "3"),
        "low": ("Low", "5"),
    }

    imp_text, priority = importance_map.get(
        importance.lower(), ("Normal", "3")
    )

    # Set ALL importance headers
    msg["Importance"] = imp_text
    msg["X-Priority"] = priority
    msg["X-MSMail-Priority"] = imp_text


    # Plain text fallback 
    msg.set_content(body)

    # HTML version
    if html_content:
        msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(current_app.MAIL_SERVER, current_app.MAIL_PORT) as server:
        server.starttls()
        server.login(current_app.MAIL_USERNAME, current_app.MAIL_PASSWORD)
        server.send_message(msg)

