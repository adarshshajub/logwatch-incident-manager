from flask import Blueprint, render_template, request
from flask_login import login_required
from app.utils.decorators import admin_required
from .parser import parse_log_file
from app.logs.analyzer import analyze_log 

log_bp = Blueprint("logs", __name__, url_prefix="/logs")

LOG_STORAGE = []

# ✅ Admin only
@log_bp.route("/upload", methods=["GET", "POST"])
@login_required
@admin_required
def upload_logs():
    global LOG_STORAGE

    if request.method == "POST":
        file = request.files.get("logfile")

        if file:
            content = file.read().decode("utf-8")

            # 🔹 Parse logs
            parsed_logs = parse_log_file(file.filename, content)

            # 🔹 Store + analyze each log
            for log in parsed_logs:
                LOG_STORAGE.append(log)

                # 🚨 Trigger alert evaluation
                analyze_log(log)

    return render_template("upload_logs.html")


# ✅ Admin + User
@log_bp.route("/search", methods=["GET", "POST"])
@login_required
def search_logs():
    results = []
    if request.method == "POST":
        keyword = request.form.get("keyword", "").lower()
        results = [
            log for log in LOG_STORAGE
            if keyword in (log["message"] or "").lower()
        ]
    return render_template("search_logs.html", results=results)
