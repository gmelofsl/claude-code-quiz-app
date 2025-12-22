"""
User model with enhanced authentication and security features.
"""

import secrets
from datetime import datetime, timedelta

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(UserMixin, db.Model):
    """
    User model for authentication and profile management.

    Enhanced with email authentication, password hashing, email verification,
    password reset, and account security features.
    """

    __tablename__ = "users"

    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Basic information
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    # Authentication
    password_hash = db.Column(
        db.String(255), nullable=True
    )  # Nullable for migration from old users

    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Email verification
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_token = db.Column(db.String(100), unique=True, nullable=True)

    # Password reset
    password_reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)

    # Account security
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    account_locked_until = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_active = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    attempts = db.relationship("Attempt", backref="user", lazy=True, cascade="all, delete-orphan")

    # Indexes and constraints
    __table_args__ = (
        db.Index("idx_user_username", "username"),
        db.Index("idx_user_email", "email"),
        db.Index("idx_user_last_active", "last_active"),
        db.CheckConstraint("failed_login_attempts >= 0", name="check_failed_attempts_positive"),
    )

    def __repr__(self):
        return f"<User {self.username}>"

    # Password management
    def set_password(self, password):
        """
        Hash and set user password using Argon2.

        Args:
            password: Plain text password
        """
        # Using Werkzeug's generate_password_hash with 'argon2' method
        # This uses argon2-cffi under the hood if installed
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        # Note: To use argon2, install argon2-cffi and use method='argon2'
        # For now using pbkdf2:sha256 for compatibility

    def check_password(self, password):
        """
        Verify password against stored hash.

        Args:
            password: Plain text password to check

        Returns:
            bool: True if password matches, False otherwise
        """
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    # Email verification
    def generate_verification_token(self):
        """
        Generate a unique email verification token.

        Returns:
            str: Verification token
        """
        self.verification_token = secrets.token_urlsafe(32)
        return self.verification_token

    def verify_email(self):
        """Mark email as verified and clear verification token."""
        self.email_verified = True
        self.verification_token = None

    # Password reset
    def generate_reset_token(self, expires_in=3600):
        """
        Generate a password reset token with expiration.

        Args:
            expires_in: Token expiration time in seconds (default: 1 hour)

        Returns:
            str: Reset token
        """
        self.password_reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(seconds=expires_in)
        return self.password_reset_token

    def verify_reset_token(self, token):
        """
        Verify password reset token is valid and not expired.

        Args:
            token: Reset token to verify

        Returns:
            bool: True if token is valid and not expired
        """
        if not self.password_reset_token or not self.reset_token_expires:
            return False

        if self.password_reset_token != token:
            return False

        if datetime.utcnow() > self.reset_token_expires:
            return False

        return True

    def clear_reset_token(self):
        """Clear password reset token after use."""
        self.password_reset_token = None
        self.reset_token_expires = None

    # Account security
    def record_failed_login(self):
        """
        Record a failed login attempt and lock account if threshold exceeded.

        Account is locked for 15 minutes after 5 failed attempts.
        """
        self.failed_login_attempts += 1

        if self.failed_login_attempts >= 5:
            self.account_locked_until = datetime.utcnow() + timedelta(minutes=15)

    def reset_failed_logins(self):
        """Reset failed login counter after successful login."""
        self.failed_login_attempts = 0
        self.account_locked_until = None

    def is_account_locked(self):
        """
        Check if account is currently locked.

        Returns:
            bool: True if account is locked
        """
        if not self.account_locked_until:
            return False

        if datetime.utcnow() > self.account_locked_until:
            # Lock period expired, clear it
            self.account_locked_until = None
            self.failed_login_attempts = 0
            return False

        return True

    def update_last_active(self):
        """Update last active timestamp."""
        self.last_active = datetime.utcnow()

    # Statistics
    def get_stats(self):
        """
        Get user statistics.

        Returns:
            dict: Statistics including total_attempts, avg_score, best_score
        """
        if not self.attempts:
            return {"total_attempts": 0, "avg_score": 0, "best_score": 0}

        completed_attempts = [a for a in self.attempts if a.completed_at is not None]
        if not completed_attempts:
            return {"total_attempts": 0, "avg_score": 0, "best_score": 0}

        percentages = [a.percentage for a in completed_attempts]
        return {
            "total_attempts": len(completed_attempts),
            "avg_score": round(sum(percentages) / len(percentages), 1),
            "best_score": round(max(percentages), 1),
        }

    # Flask-Login required methods
    def get_id(self):
        """Return user ID as string for Flask-Login."""
        return str(self.id)

    @property
    def is_authenticated(self):
        """Return True if user is authenticated."""
        return True

    @property
    def is_anonymous(self):
        """Return False as this is not an anonymous user."""
        return False
