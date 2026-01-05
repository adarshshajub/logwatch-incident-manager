from app.utils.servicenow_client import create_incident
from app.utils.template_renderer import render_template_string
from app.models.alert_execution import AlertExecution
from app.extensions import db


def execute_servicenow_action(alert, action_config, log_data):
    try:
        context = {
            "alert_name": alert.name,
            "keyword": alert.keyword,
            "log_message": log_data.message,
            "timestamp": log_data.timestamp,
        }

        payload = {
            "short_description": render_template_string(
                action_config["short_description"], context
            ),
            "description": render_template_string(
                f"{action_config["description"]}", context
            ),
            "priority": action_config.get("priority", "3"),
        }

        result = create_incident(payload)

        incident_number = result["result"].get("number", "UNKNOWN")

        db.session.add(AlertExecution(
            alert_id=alert.id,
            action_type="servicenow",
            status="SUCCESS",
            message=f"Incident {incident_number} created"
        ))

    except Exception as e:
        db.session.add(AlertExecution(
            alert_id=alert.id,
            action_type="servicenow",
            status="FAILED",
            message=str(e)
        ))

    db.session.commit()
