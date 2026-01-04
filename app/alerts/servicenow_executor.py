from app.utils.servicenow_client import create_incident
from app.utils.template_renderer import render_template_string


def execute_servicenow_action(alert, action_config, log_data):
    context = {
        "alert_name": alert.name,
        "keyword": alert.keyword,
        "log_message": log_data.get("message"),
        "timestamp": log_data.get("timestamp"),
    }

    short_description = render_template_string(
        action_config["short_description"], context
    )

    description = render_template_string(
        action_config["description"], context
    )

    payload = {
        "short_description": short_description,
        "description": description,
        "priority": action_config.get("priority", "3"),
    }

    # Optional fields
    if action_config.get("assignment_group"):
        payload["assignment_group"] = action_config["assignment_group"]

    if action_config.get("category"):
        payload["category"] = action_config["category"]

    create_incident(payload)
