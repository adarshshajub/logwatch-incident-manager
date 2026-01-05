from app.alerts.email_executor import execute_email_action
from app.alerts.servicenow_executor import execute_servicenow_action
from app.alerts.throttle import is_throttled, record_execution


def process_log_for_alerts(alert, log_data):
    for action in alert.actions:
        if not action.enabled:
            continue

        throttle_minutes = action.config.get("throttle_minutes")

        # 🚫 Dedup / Throttle check
        if is_throttled(alert.id, action.action_type, throttle_minutes):
            continue

        # 📧 Email
        if action.action_type == "email":
            execute_email_action(alert, action.config, log_data)
            # record_execution(alert.id, "email")

        # 🎫 ServiceNow
        if action.action_type == "servicenow":
            execute_servicenow_action(alert, action.config, log_data)
            # record_execution(alert.id, "servicenow")
