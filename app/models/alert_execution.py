from app.extensions import db
from datetime import datetime


class AlertExecution(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    alert_id = db.Column(
        db.Integer,
        db.ForeignKey("alert_config.id"),
        nullable=False
    )

    action_type = db.Column(db.String(50), nullable=False)

    status = db.Column(db.String(20), nullable=False)

    message = db.Column(db.Text)

    triggered_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,   # ✅ default only
        nullable=False
    )
    
