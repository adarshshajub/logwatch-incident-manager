from app.models.alert_config import AlertConfig
from app.alerts.executor import process_log_for_alerts
from app.models.log_entry import LogEntry


def analyze_log(log_data):
    alerts = AlertConfig.query.filter_by(enabled=True).all()

    for alert in alerts:
        if alert.keyword.lower() in log_data["message"].lower():
            process_log_for_alerts(alert, log_data)

def analyze_logs_for_alert(alert):
    logs = LogEntry.query.all()
    for log in logs:
        if alert.keyword.lower() in log.message.lower():
            process_log_for_alerts(alert, log)

