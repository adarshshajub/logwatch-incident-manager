from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.utils.decorators import admin_required
from .parser import parse_log_file
from app.models.log_source import LogSource
from app.extensions import db
from app.models.log_entry import LogEntry


log_bp = Blueprint("logs", __name__, url_prefix="/logs")

# Admin only
@log_bp.route("/add-source", methods=["GET", "POST"])
@login_required
@admin_required
def add_log_source():
    if request.method == "POST":
        name = request.form["name"]
        file_path = request.form["file_path"]

        source = LogSource(
            name=name,
            file_path=file_path
        )
        db.session.add(source)
        db.session.commit()

        flash("Log source added successfully", "success")
        return redirect(url_for("logs.add_log_source"))

    return render_template("add_log_source.html")


@log_bp.route("/sources")
@login_required
@admin_required
def list_log_sources():
    sources = LogSource.query.order_by(LogSource.id.desc()).all()
    return render_template("log_sources.html", sources=sources)


@log_bp.route("/sources/toggle/<int:source_id>")
@login_required
@admin_required
def toggle_log_source(source_id):
    source = LogSource.query.get_or_404(source_id)
    source.enabled = not source.enabled
    db.session.commit()
    return redirect(url_for("logs.list_log_sources"))

@log_bp.route("/sources/edit/<int:source_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_log_source(source_id):
    source = LogSource.query.get_or_404(source_id)

    if request.method == "POST":
        new_name = request.form["name"]
        new_path = request.form["file_path"]
        enabled = "enabled" in request.form
        reset_offset = "reset_offset" in request.form

        # Detect path change
        path_changed = new_path != source.file_path

        source.name = new_name
        source.file_path = new_path
        source.enabled = enabled

        # Reset offset if requested OR path changed
        if reset_offset or path_changed:
            source.last_read_offset = 0

        db.session.commit()

        flash("Log source updated successfully", "success")
        return redirect(url_for("logs.list_log_sources"))

    return render_template("edit_log_source.html", source=source)


# Admin + User
@log_bp.route("/search", methods=["GET", "POST"])
@login_required
def search_logs():
    results = []

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

        if keyword:
            results = LogEntry.query.filter(
                LogEntry.message.ilike(f"%{keyword}%")
            ).order_by(LogEntry.created_at.desc()).all()

    return render_template("search_logs.html", results=results)
