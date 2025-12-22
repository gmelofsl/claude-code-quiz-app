"""
Unit tests for service layer.

Tests business logic in service classes.
"""

from datetime import datetime, timedelta

import pytest

from app.extensions import db
from app.models import User
from app.services.auth_service import AuthService
from tests.factories import LockedUserFactory, UnverifiedUserFactory, UserFactory


@pytest.mark.unit
@pytest.mark.services
class TestAuthService:
    """Tests for AuthService."""

    def test_register_user_success(self, app):
        """Test successful user registration."""
        with app.app_context():
            user, error = AuthService.register_user(
                username="newuser", email="newuser@example.com", password="SecurePass123"
            )

            assert error is None
            assert user is not None
            assert user.username == "newuser"
            assert user.email == "newuser@example.com"
            assert user.password_hash is not None
            assert user.is_active is True
            assert user.email_verified is False
            assert user.verification_token is not None

    def test_register_user_duplicate_username(self, app):
        """Test registration with existing username."""
        with app.app_context():
            UserFactory(username="existinguser")
            db.session.commit()

            user, error = AuthService.register_user(
                username="existinguser", email="newemail@example.com", password="SecurePass123"
            )

            assert user is None
            assert "username" in error.lower()

    def test_register_user_duplicate_email(self, app):
        """Test registration with existing email."""
        with app.app_context():
            UserFactory(email="existing@example.com")
            db.session.commit()

            user, error = AuthService.register_user(
                username="newuser", email="existing@example.com", password="SecurePass123"
            )

            assert user is None
            assert "email" in error.lower()

    def test_authenticate_user_success(self, app):
        """Test successful authentication with username."""
        with app.app_context():
            user = UserFactory(username="testuser")
            user.set_password("TestPass123")
            db.session.commit()

            auth_user, error = AuthService.authenticate_user(
                username_or_email="testuser", password="TestPass123"
            )

            assert error is None
            assert auth_user is not None
            assert auth_user.id == user.id
            assert auth_user.failed_login_attempts == 0

    def test_authenticate_user_with_email(self, app):
        """Test successful authentication with email."""
        with app.app_context():
            user = UserFactory(email="test@example.com")
            user.set_password("TestPass123")
            db.session.commit()

            auth_user, error = AuthService.authenticate_user(
                username_or_email="test@example.com", password="TestPass123"
            )

            assert error is None
            assert auth_user is not None
            assert auth_user.id == user.id

    def test_authenticate_user_wrong_password(self, app):
        """Test authentication with incorrect password."""
        with app.app_context():
            user = UserFactory(username="testuser")
            user.set_password("TestPass123")
            db.session.commit()

            auth_user, error = AuthService.authenticate_user(
                username_or_email="testuser", password="WrongPassword"
            )

            assert auth_user is None
            assert error is not None
            assert "invalid" in error.lower()

            # Check failed login attempt was recorded
            db.session.refresh(user)
            assert user.failed_login_attempts == 1

    def test_authenticate_user_nonexistent(self, app):
        """Test authentication with non-existent user."""
        with app.app_context():
            auth_user, error = AuthService.authenticate_user(
                username_or_email="nonexistent", password="AnyPassword"
            )

            assert auth_user is None
            assert error is not None

    def test_authenticate_user_account_locked(self, app):
        """Test authentication with locked account."""
        with app.app_context():
            user = LockedUserFactory(username="lockeduser")
            user.set_password("TestPass123")
            db.session.commit()

            auth_user, error = AuthService.authenticate_user(
                username_or_email="lockeduser", password="TestPass123"
            )

            assert auth_user is None
            assert error is not None
            assert "locked" in error.lower()

    def test_authenticate_user_inactive(self, app):
        """Test authentication with inactive account."""
        with app.app_context():
            user = UserFactory(username="inactive", is_active=False)
            user.set_password("TestPass123")
            db.session.commit()

            auth_user, error = AuthService.authenticate_user(
                username_or_email="inactive", password="TestPass123"
            )

            assert auth_user is None
            assert error is not None
            assert "inactive" in error.lower() or "deactivated" in error.lower()

    def test_verify_email_success(self, app):
        """Test successful email verification."""
        with app.app_context():
            user = UnverifiedUserFactory()
            token = user.verification_token
            db.session.commit()

            success, message = AuthService.verify_email(token)

            assert success is True
            assert "success" in message.lower() or "verified" in message.lower()

            db.session.refresh(user)
            assert user.email_verified is True
            assert user.verification_token is None

    def test_verify_email_invalid_token(self, app):
        """Test email verification with invalid token."""
        with app.app_context():
            success, message = AuthService.verify_email("invalid_token")

            assert success is False
            assert "invalid" in message.lower()

    def test_verify_email_already_verified(self, app):
        """Test email verification for already verified user."""
        with app.app_context():
            _ = UserFactory(email_verified=True, verification_token="old_token")
            db.session.commit()

            success, message = AuthService.verify_email("old_token")

            assert success is False
            assert "already" in message.lower()

    def test_request_password_reset_success(self, app):
        """Test successful password reset request."""
        with app.app_context():
            user = UserFactory(email="test@example.com")
            db.session.commit()

            success, message = AuthService.request_password_reset("test@example.com")

            assert success is True
            assert "sent" in message.lower() or "instructions" in message.lower()

            db.session.refresh(user)
            assert user.password_reset_token is not None
            assert user.reset_token_expires is not None
            assert user.reset_token_expires > datetime.utcnow()

    def test_request_password_reset_nonexistent_email(self, app):
        """Test password reset for non-existent email."""
        with app.app_context():
            success, message = AuthService.request_password_reset("nonexistent@example.com")

            # Should return success to prevent email enumeration
            assert success is True

    def test_reset_password_success(self, app):
        """Test successful password reset."""
        with app.app_context():
            user = UserFactory()
            token = user.generate_reset_token()
            old_password_hash = user.password_hash
            db.session.commit()

            success, message = AuthService.reset_password(
                token=token, new_password="NewSecurePass123"
            )

            assert success is True
            assert "success" in message.lower() or "reset" in message.lower()

            db.session.refresh(user)
            assert user.password_hash != old_password_hash
            assert user.check_password("NewSecurePass123") is True
            assert user.password_reset_token is None
            assert user.reset_token_expires is None

    def test_reset_password_invalid_token(self, app):
        """Test password reset with invalid token."""
        with app.app_context():
            success, message = AuthService.reset_password(
                token="invalid_token", new_password="NewPassword123"
            )

            assert success is False
            assert "invalid" in message.lower() or "expired" in message.lower()

    def test_reset_password_expired_token(self, app):
        """Test password reset with expired token."""
        with app.app_context():
            user = UserFactory()
            token = user.generate_reset_token()
            user.reset_token_expires = datetime.utcnow() - timedelta(hours=1)
            db.session.commit()

            success, message = AuthService.reset_password(
                token=token, new_password="NewPassword123"
            )

            assert success is False
            assert "expired" in message.lower()

    def test_change_password_success(self, app):
        """Test successful password change."""
        with app.app_context():
            user = UserFactory()
            user.set_password("OldPass123")
            old_password_hash = user.password_hash
            db.session.commit()

            success, message = AuthService.change_password(
                user=user, current_password="OldPass123", new_password="NewPass123"
            )

            assert success is True
            assert "success" in message.lower() or "changed" in message.lower()

            db.session.refresh(user)
            assert user.password_hash != old_password_hash
            assert user.check_password("NewPass123") is True

    def test_change_password_wrong_current(self, app):
        """Test password change with wrong current password."""
        with app.app_context():
            user = UserFactory()
            user.set_password("OldPass123")
            db.session.commit()

            success, message = AuthService.change_password(
                user=user, current_password="WrongPassword", new_password="NewPass123"
            )

            assert success is False
            assert "current" in message.lower() or "incorrect" in message.lower()

    def test_update_profile_success(self, app):
        """Test successful profile update."""
        with app.app_context():
            user = UserFactory(username="olduser", email="old@example.com")
            db.session.commit()

            success, message = AuthService.update_profile(
                user=user, username="newuser", email="new@example.com"
            )

            assert success is True
            assert "success" in message.lower() or "updated" in message.lower()

            db.session.refresh(user)
            assert user.username == "newuser"
            assert user.email == "new@example.com"

    def test_update_profile_duplicate_username(self, app):
        """Test profile update with duplicate username."""
        with app.app_context():
            UserFactory(username="existinguser")
            user = UserFactory(username="myuser")
            db.session.commit()

            success, message = AuthService.update_profile(
                user=user, username="existinguser", email="new@example.com"
            )

            assert success is False
            assert "username" in message.lower()

    def test_update_profile_duplicate_email(self, app):
        """Test profile update with duplicate email."""
        with app.app_context():
            UserFactory(email="existing@example.com")
            user = UserFactory(email="myemail@example.com")
            db.session.commit()

            success, message = AuthService.update_profile(
                user=user, username="newusername", email="existing@example.com"
            )

            assert success is False
            assert "email" in message.lower()

    def test_update_profile_no_changes(self, app):
        """Test profile update with no actual changes."""
        with app.app_context():
            user = UserFactory(username="myuser", email="myemail@example.com")
            db.session.commit()

            success, message = AuthService.update_profile(
                user=user, username="myuser", email="myemail@example.com"
            )

            assert success is True
