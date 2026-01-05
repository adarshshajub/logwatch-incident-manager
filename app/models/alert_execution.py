from app.extensions import db
from datetime import datetime


class AlertExecution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(50), nullable=False)  # email / servicenow
    status = db.Column(db.String(20), nullable=False, default="SUCCESS")
    message = db.Column(db.Text, nullable=True)  # error / incident number
    triggered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
