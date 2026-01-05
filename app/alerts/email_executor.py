from app.utils.email_service import send_email
from app.utils.template_renderer import render_template_string
from app.models.alert_execution import AlertExecution
from app.extensions import db

def execute_email_action(alert, action_config, log_data):
    try:
        context = {
            "alert_name": alert.name,
            "keyword": alert.keyword,
            "log_message": log_data.message,
            "timestamp": log_data.timestamp,
        }

        subject = render_template_string(
            action_config["subject"], context
        )

        email_body = ""
        if action_config["include_log"] == "true":
            email_body = f"""{action_config["body"]}
                    timestamp: { log_data.message }
                    message: { log_data.timestamp }
            """
        else:
            email_body=action_config["body"] 
            
        body = render_template_string(
            email_body, context
        )

        send_email(
            to_addresses=action_config["to"],
            subject=subject,
            body=body,
            importance=action_config.get("importance", "normal")
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