from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.extensions import db
from .models import User
from app.models.log_source import LogSource
from app.models.log_entry import LogEntry
from app.models.alert_config import AlertConfig

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
    "dashboard.html",
    log_count=LogEntry.query.count(),
    alert_count=AlertConfig.query.filter_by(enabled=True).count(),
    source_count=LogSource.query.filter_by(enabled=True).count(),
)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
