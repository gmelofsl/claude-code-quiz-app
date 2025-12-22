"""
Dashboard routes blueprint.

Handles the main dashboard view for logged-in users.
"""

from flask import Blueprint, render_template
from flask_login import current_user, login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def index():
    """
    Main dashboard page.

    Shows user stats, available quizzes, and recent activity.
    """
    return render_template("dashboard/index.html", user=current_user)
