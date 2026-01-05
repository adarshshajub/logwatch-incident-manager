from app.extensions import db
from datetime import datetime


class AlertRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    alert_id = db.Column(db.Integer, unique=True, nullable=False)

    last_run_at = db.Column(db.DateTime, nullable=True)