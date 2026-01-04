from datetime import datetime, timedelta
from app.models.alert_execution import AlertExecution
from app.extensions import db


def is_throttled(alert_id, action_type, throttle_minutes):
    if not throttle_minutes:
        return False

    record = AlertExecution.query.filter_by(
        alert_id=alert_id,
        action_type=action_type
    ).first()

    if not record:
        return False

    next_allowed_time = record.last_triggered_at + timedelta(minutes=throttle_minutes)
    return datetime.utcnow() < next_allowed_time


def record_execution(alert_id, action_type):
    now = datetime.utcnow()

    record = AlertExecution.query.filter_by(
        alert_id=alert_id,
        action_type=action_type
    ).first()

    if record:
        record.last_triggered_at = now
    else:
        db.session.add(AlertExecution(
            alert_id=alert_id,
            action_type=action_type,
            last_triggered_at=now
        ))

    db.session.commit()
