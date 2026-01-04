from app.utils.email_service import send_email
from app.utils.template_renderer import render_template_string


def execute_email_action(alert, action_config, log_data):
    context = {
        "alert_name": alert.name,
        "keyword": alert.keyword,
        "log_message": log_data.get("message"),
        "timestamp": log_data.get("timestamp"),
    }

    subject = render_template_string(
        action_config["subject"], context
    )

    body = render_template_string(
        action_config["body"], context
    )

    send_email(
        to_addresses=action_config["to"],
        subject=subject,
        body=body,
        importance=action_config.get("importance", "normal")
    )
