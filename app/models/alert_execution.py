from app.extensions import db
from datetime import datetime


class AlertExecution(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    alert_id = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(50), nullable=False)

    last_triggered_at = db.Column(db.DateTime, nullable=False)
