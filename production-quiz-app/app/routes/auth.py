"""
Authentication routes blueprint.

Handles user registration, login, logout, password reset, email verification, etc.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import limiter
from app.forms.auth_forms import (
    ChangePasswordForm,
    ForgotPasswordForm,
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
    UpdateProfileForm,
)
from app.services.auth_service import AuthService

# Create blueprint
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("3 per hour")  # Rate limit: 3 registrations per hour per IP
def register():
    """User registration page."""
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Register user
        user, error = AuthService.register_user(
            username=form.username.data, email=form.email.data, password=form.password.data
        )

        if error:
            flash(error, "danger")
        else:
            # Send verification email
            AuthService.send_verification_email(user)

            flash(
                "Registration successful! Please check your email to verify your account.",
                "success",
            )
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per 15 minutes")  # Rate limit: 5 login attempts per 15 minutes per IP
def login():
    """User login page."""
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()

    if form.validate_on_submit():
        # Authenticate user
        user, error = AuthService.authenticate_user(
            username_or_email=form.username_or_email.data, password=form.password.data
        )

        if error:
            flash(error, "danger")
        else:
            # Log user in
            login_user(user, remember=form.remember_me.data)

            # Check if email is verified
            if not user.email_verified:
                flash("Please verify your email address to access all features.", "warning")

            flash(f"Welcome back, {user.username}!", "success")

            # Redirect to next page or dashboard
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("dashboard.index"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """User logout."""
    username = current_user.username
    logout_user()
    flash(f"Goodbye, {username}! You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/verify/<token>")
def verify_email(token):
    """Verify user email with token."""
    success, message = AuthService.verify_email(token)

    if success:
        flash(message, "success")
        return redirect(url_for("auth.login"))
    else:
        flash(message, "danger")
        return redirect(url_for("auth.register"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
@limiter.limit("3 per hour")  # Rate limit: 3 password reset requests per hour per IP
def forgot_password():
    """Forgot password page - request password reset."""
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        # Request password reset
        user, error = AuthService.request_password_reset(email=form.email.data)

        # Always show success message for security
        # (Don't reveal if email exists or not)
        if user:
            AuthService.send_password_reset_email(user)

        flash("If your email is registered, you will receive password reset instructions.", "info")
        return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html", form=form)


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Reset password with token."""
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        # Reset password
        success, message = AuthService.reset_password(token=token, new_password=form.password.data)

        if success:
            flash(message, "success")
            return redirect(url_for("auth.login"))
        else:
            flash(message, "danger")

    return render_template("auth/reset_password.html", form=form, token=token)


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User profile page - view and edit profile."""
    update_form = UpdateProfileForm(
        original_username=current_user.username, original_email=current_user.email
    )
    change_password_form = ChangePasswordForm()

    # Pre-populate form with current data
    if request.method == "GET":
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email

    # Handle profile update
    if update_form.validate_on_submit() and "update_profile" in request.form:
        success, message = AuthService.update_profile(
            user=current_user, username=update_form.username.data, email=update_form.email.data
        )

        if success:
            flash(message, "success")
            return redirect(url_for("auth.profile"))
        else:
            flash(message, "danger")

    # Handle password change
    if change_password_form.validate_on_submit() and "change_password" in request.form:
        success, message = AuthService.change_password(
            user=current_user,
            current_password=change_password_form.current_password.data,
            new_password=change_password_form.new_password.data,
        )

        if success:
            flash(message, "success")
            return redirect(url_for("auth.profile"))
        else:
            flash(message, "danger")

    # Get user stats for display
    stats = current_user.get_stats()

    return render_template(
        "auth/profile.html",
        update_form=update_form,
        change_password_form=change_password_form,
        stats=stats,
    )


@auth_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    """Change password (separate endpoint for API/AJAX)."""
    form = ChangePasswordForm()

    if form.validate_on_submit():
        success, message = AuthService.change_password(
            user=current_user,
            current_password=form.current_password.data,
            new_password=form.new_password.data,
        )

        if success:
            flash(message, "success")
        else:
            flash(message, "danger")

    return redirect(url_for("auth.profile"))


# Error handlers for this blueprint


@auth_bp.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded."""
    flash("Too many requests. Please try again later.", "warning")
    return render_template("errors/429.html"), 429


@auth_bp.errorhandler(404)
def not_found(e):
    """Handle 404 errors in auth routes."""
    flash("Page not found.", "danger")
    return redirect(url_for("auth.login"))


# Helper function for redirecting unauthenticated users


def login_required_message():
    """Flash message for login required."""
    flash("Please log in to access this page.", "warning")
    return redirect(url_for("auth.login"))
