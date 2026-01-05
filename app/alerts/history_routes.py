from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.alert_execution import AlertExecution
from app.models.alert_config import AlertConfig

history_bp = Blueprint("history", __name__, url_prefix="/alerts/history")


@history_bp.route("/")
@login_required
def alert_history():
    if current_user.role == "admin":
        history = AlertExecution.query.order_by(
            AlertExecution.triggered_at.desc()
        ).all()
    else:
        user_alerts = AlertConfig.query.filter_by(
            user_id=current_user.id
        ).with_entities(AlertConfig.id).subquery()

        history = AlertExecution.query.filter(
            AlertExecution.alert_id.in_(user_alerts)
        ).order_by(AlertExecution.triggered_at.desc()).all()

    return render_template("alert_history.html", history=history)
