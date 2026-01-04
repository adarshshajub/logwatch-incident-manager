from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models.alert_config import AlertConfig
import json
from app.models.alert_action import AlertAction 

alert_bp = Blueprint("alerts", __name__, url_prefix="/alerts")

@alert_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_alert():
    if request.method == "POST":
        keyword = request.form["keyword"]

        # 🔥 Get multiple actions
        actions = request.form.getlist("actions")
        if not actions:
            return "At least one action must be selected", 400

        alert = AlertConfig(
            name=request.form["name"],
            keyword=request.form["keyword"],
            user_id=current_user.id,
            interval_minutes=int(request.form["interval_minutes"]),
        )
        db.session.add(alert)
        db.session.flush()  # get alert.id

        # Email action
        if "email_action" in request.form:
            email_config = {
                "to": request.form["email_to"].split(","),
                "subject": request.form["email_subject"],
                "body": request.form["email_body"],
                "importance": request.form["email_importance"],
                "include_log": "email_include_log" in request.form,
                "throttle_minutes": int(request.form.get("email_throttle") or 0)
            }

            db.session.add(AlertAction(
                alert_id=alert.id,
                action_type="email",
                config=email_config
            ))

        # ServiceNow action
        if "sn_action" in request.form:
            sn_config = {
                "priority": request.form["sn_priority"],
                "short_description": request.form["sn_short_desc"],
                "description": request.form["sn_description"],
                "include_log": "sn_include_log" in request.form,
                "throttle_minutes": int(request.form.get("email_throttle") or 0)
            }

            db.session.add(AlertAction(
                alert_id=alert.id,
                action_type="servicenow",
                config=sn_config
            ))

        db.session.commit()

        return redirect(url_for("alerts.my_alerts"))

    return render_template("create_alert.html")


@alert_bp.route("/my-alerts")
@login_required
def my_alerts():
    if current_user.role == "admin":
        alerts = AlertConfig.query.all()
    else:
        alerts = AlertConfig.query.filter_by(user_id=current_user.id).all()

    return render_template("my_alerts.html", alerts=alerts)

