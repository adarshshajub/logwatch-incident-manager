from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.alert_config import AlertConfig
import json
from app.models.alert_action import AlertAction 
from app.models.log_entry import LogEntry

alert_bp = Blueprint("alerts", __name__, url_prefix="/alerts")

@alert_bp.route("/")
@login_required
def list_alerts():
    """
    Admin → sees all alerts
    User  → sees only their alerts
    """
    if current_user.role == "admin":
        alerts = AlertConfig.query.order_by(AlertConfig.id.desc()).all()
    else:
        alerts = AlertConfig.query.filter_by(
            user_id=current_user.id
        ).order_by(AlertConfig.id.desc()).all()

    return render_template("alert_list.html", alerts=alerts)


@alert_bp.route("/toggle/<int:alert_id>")
@login_required
def toggle_alert(alert_id):
    alert = AlertConfig.query.get_or_404(alert_id)

    # Users can toggle only their own alerts
    if current_user.role != "admin" and alert.user_id != current_user.id:
        return "Unauthorized", 403

    alert.enabled = not alert.enabled
    db.session.commit()

    return redirect(url_for("alerts.list_alerts"))

@alert_bp.route("/edit/<int:alert_id>", methods=["GET", "POST"])
@login_required
def edit_alert(alert_id):
    alert = AlertConfig.query.get_or_404(alert_id)

    # Security: user can edit only own alerts (admin can edit all)
    if current_user.role != "admin" and alert.user_id != current_user.id:
        return "Unauthorized", 403

    if request.method == "POST":
        alert.name = request.form["name"]
        alert.keyword = request.form["keyword"]
        alert.interval_minutes = int(request.form["interval_minutes"])
        alert.enabled = "enabled" in request.form

        db.session.commit()
        flash("Alert updated successfully", "success")
        return redirect(url_for("alerts.list_alerts"))

    return render_template("edit_alert.html", alert=alert)

@alert_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_alert():
    if request.method == "POST":
        keyword = request.form["keyword"].strip()

        # 🔥 Get multiple actions
        email_selected = "email_action" in request.form
        email_log_include = "email_include_log" in request.form
        sn_selected = "sn_action" in request.form
        sn_log_include = "sn_include_log" in request.form

        if not email_selected and not sn_selected:
            return "At least one action must be selected", 400

        alert = AlertConfig(
            name=request.form["name"],
            keyword=request.form["keyword"],
            user_id=current_user.id,
            interval_minutes=int(request.form["interval_minutes"]),
        )
        db.session.add(alert)
        db.session.flush()  # get alert.id

        search_request = None
        if keyword:
            results = LogEntry.query.filter(
                LogEntry.message.ilike(f"%{keyword}%")
            ).order_by(LogEntry.created_at.desc()).all()

            search_request = f"""
                    <table class="table table-striped">
                        <thead>
                        <tr>
                            <th>Time</th>
                            <th>Message</th>
                        </tr>
                        </thead>
                        <tbody>
                    """
            
            for result in results:
                search_request += f"""
                        <tr>
                            <td>{ result.timestamp }</td>
                            <td>{ result.message }</td>
                        </tr>
                    """
            
            search_request += """ </tbody>
                    </table>"""

        # Email action
        if "email_action" in request.form:
            email_config = {
                "to": request.form["email_to"].split(","),
                "subject": request.form["email_subject"],
                "body": request.form["email_body"],
                "importance": request.form["email_importance"],
                "throttle_minutes": int(request.form.get("email_throttle") or 0)
            }

            if email_log_include:
                email_config["search_content"] = search_request

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
                "throttle_minutes": int(request.form.get("sn_throttle") or 0)
            }

            if sn_log_include:
                sn_config["search_content"] = search_request

            db.session.add(AlertAction(
                alert_id=alert.id,
                action_type="servicenow",
                config=sn_config
            ))

        db.session.commit()

        return redirect(url_for("alerts.list_alerts"))

    return render_template("create_alert.html")


@alert_bp.route("/my-alerts")
@login_required
def my_alerts():
    if current_user.role == "admin":
        alerts = AlertConfig.query.all()
    else:
        alerts = AlertConfig.query.filter_by(user_id=current_user.id).all()

    return render_template("my_alerts.html", alerts=alerts)

