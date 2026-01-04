from app.models.alert_config import AlertConfig
from app.alerts.executor import process_log_for_alerts


def analyze_log(log_data):
    alerts = AlertConfig.query.filter_by(enabled=True).all()

    for alert in alerts:
        if alert.keyword.lower() in log_data["message"].lower():
            process_log_for_alerts(alert, log_data)