from app.utils.email_service import send_email
from app.utils.template_renderer import render_template_string
from app.models.alert_execution import AlertExecution
from app.extensions import db
from email.message import EmailMessage
import smtplib
from app.config import Config


def execute_email_action(alert, action_config, log_data):
    try:
        context = {
            "alert_name": alert.name,
            "keyword": alert.keyword,
            "log_message": log_data.message,
            "timestamp": log_data.timestamp,
        }

        subject = action_config["subject"]
        body = action_config["body"]
        html = f"<div> {body.replace("\n", "<br>")} </div> {action_config["search_content"]}"

        send_email(
            to=action_config["to"],
            subject=subject,
            body=body,
            html_content=html,
            importance=action_config["importance"],
        )

        db.session.add(AlertExecution(
            alert_id=alert.id,
            action_type="email",
            status="SUCCESS",
            message="Email sent successfully"
        ))

    except Exception as e:
        db.session.add(AlertExecution(
            alert_id=alert.id,
            action_type="email",
            status="FAILED",
            message=str(e)
        ))

    db.session.commit()


