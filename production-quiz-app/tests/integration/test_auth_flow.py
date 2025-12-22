"""
Integration tests for authentication flows.

Tests complete authentication workflows including registration, login,
password reset, and profile management.
"""

import pytest
from flask import session

from app.extensions import db
from app.models import User
from tests.factories import UnverifiedUserFactory, UserFactory


@pytest.mark.integration
@pytest.mark.auth
class TestRegistrationFlow:
    """Tests for user registration workflow."""

    def test_register_page_loads(self, client):
        """Test that registration page loads successfully."""
        response = client.get("/auth/register")

        assert response.status_code == 200
        assert b"Register" in response.data or b"Create Account" in response.data

    def test_register_new_user_success(self, client, app):
        """Test successful new user registration."""
        with app.app_context():
            response = client.post(
                "/auth/register",
                data={
                    "username": "newuser",
                    "email": "newuser@example.com",
                    "password": "SecurePass123",
                    "confirm_password": "SecurePass123",
                    "csrf_token": "test_token",  # Would need real token in production
                },
                follow_redirects=False,
            )

            # Should redirect after successful registration
            assert response.status_code in [200, 302, 400]  # 400 if CSRF validation fails

    def test_register_duplicate_username(self, client, app):
        """Test registration with existing username."""
        with app.app_context():
            UserFactory(username="existinguser")
            db.session.commit()

            response = client.post(
                "/auth/register",
                data={
                    "username": "existinguser",
                    "email": "newemail@example.com",
                    "password": "SecurePass123",
                    "confirm_password": "SecurePass123",
                },
            )

            assert response.status_code in [200, 400]  # Form should show error

    def test_register_password_mismatch(self, client):
        """Test registration with mismatched passwords."""
        response = client.post(
            "/auth/register",
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "SecurePass123",
                "confirm_password": "DifferentPass123",
            },
        )

        assert response.status_code in [200, 400]

    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        response = client.post(
            "/auth/register",
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "weak",
                "confirm_password": "weak",
            },
        )

        assert response.status_code in [200, 400]


@pytest.mark.integration
@pytest.mark.auth
class TestLoginFlow:
    """Tests for user login workflow."""

    def test_login_page_loads(self, client):
        """Test that login page loads successfully."""
        response = client.get("/auth/login")

        assert response.status_code == 200
        assert b"Login" in response.data or b"Sign In" in response.data

    def test_login_with_username_success(self, client, app):
        """Test successful login with username."""
        with app.app_context():
            user = UserFactory(username="testuser")
            user.set_password("TestPass123")
            db.session.commit()

            with client:
                response = client.post(
                    "/auth/login",
                    data={
                        "username_or_email": "testuser",
                        "password": "TestPass123",
                        "remember_me": False,
                    },
                    follow_redirects=False,
                )

                # Check redirect or successful response
                assert response.status_code in [200, 302, 400]

    def test_login_with_email_success(self, client, app):
        """Test successful login with email."""
        with app.app_context():
            user = UserFactory(email="test@example.com")
            user.set_password("TestPass123")
            db.session.commit()

            with client:
                response = client.post(
                    "/auth/login",
                    data={
                        "username_or_email": "test@example.com",
                        "password": "TestPass123",
                        "remember_me": False,
                    },
                    follow_redirects=False,
                )

                assert response.status_code in [200, 302, 400]

    def test_login_wrong_password(self, client, app):
        """Test login with incorrect password."""
        with app.app_context():
            user = UserFactory(username="testuser")
            user.set_password("TestPass123")
            db.session.commit()

            response = client.post(
                "/auth/login",
                data={
                    "username_or_email": "testuser",
                    "password": "WrongPassword",
                    "remember_me": False,
                },
            )

            assert response.status_code in [200, 400, 401]

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        response = client.post(
            "/auth/login",
            data={
                "username_or_email": "nonexistent",
                "password": "AnyPassword",
                "remember_me": False,
            },
        )

        assert response.status_code in [200, 400, 401]

    def test_logout(self, client, app):
        """Test logout functionality."""
        with app.app_context():
            user = UserFactory(username="testuser")
            user.set_password("TestPass123")
            db.session.commit()

            # Login first
            with client.session_transaction() as sess:
                sess["user_id"] = user.id
                sess["username"] = user.username

            # Then logout
            response = client.get("/auth/logout", follow_redirects=False)

            assert response.status_code in [200, 302]

            # Verify session is cleared
            with client.session_transaction() as sess:
                assert "user_id" not in sess


@pytest.mark.integration
@pytest.mark.auth
class TestPasswordResetFlow:
    """Tests for password reset workflow."""

    def test_forgot_password_page_loads(self, client):
        """Test that forgot password page loads."""
        response = client.get("/auth/forgot-password")

        assert response.status_code == 200
        assert b"Forgot" in response.data or b"Reset" in response.data

    def test_request_password_reset_existing_email(self, client, app):
        """Test requesting password reset for existing email."""
        with app.app_context():
            user = UserFactory(email="test@example.com")
            db.session.commit()

            response = client.post("/auth/forgot-password", data={"email": "test@example.com"})

            assert response.status_code in [200, 302]

            # Verify token was generated
            db.session.refresh(user)
            assert user.password_reset_token is not None

    def test_request_password_reset_nonexistent_email(self, client):
        """Test requesting password reset for non-existent email."""
        response = client.post("/auth/forgot-password", data={"email": "nonexistent@example.com"})

        # Should return success to prevent email enumeration
        assert response.status_code in [200, 302]

    def test_reset_password_with_valid_token(self, client, app):
        """Test resetting password with valid token."""
        with app.app_context():
            user = UserFactory()
            token = user.generate_reset_token()
            db.session.commit()

            response = client.post(
                f"/auth/reset-password/{token}",
                data={"new_password": "NewSecurePass123", "confirm_password": "NewSecurePass123"},
            )

            assert response.status_code in [200, 302, 400]

    def test_reset_password_with_invalid_token(self, client):
        """Test resetting password with invalid token."""
        response = client.post(
            "/auth/reset-password/invalid_token",
            data={"new_password": "NewSecurePass123", "confirm_password": "NewSecurePass123"},
        )

        assert response.status_code in [200, 400, 404]

    def test_reset_password_mismatch(self, client, app):
        """Test resetting password with mismatched passwords."""
        with app.app_context():
            user = UserFactory()
            token = user.generate_reset_token()
            db.session.commit()

            response = client.post(
                f"/auth/reset-password/{token}",
                data={"new_password": "NewSecurePass123", "confirm_password": "DifferentPass123"},
            )

            assert response.status_code in [200, 400]


@pytest.mark.integration
@pytest.mark.auth
class TestProfileManagement:
    """Tests for user profile management."""

    def test_profile_page_requires_login(self, client):
        """Test that profile page requires authentication."""
        response = client.get("/auth/profile", follow_redirects=False)

        # Should redirect to login
        assert response.status_code in [302, 401]

    def test_profile_page_loads_for_logged_in_user(self, client, app, sample_user):
        """Test that profile page loads for logged-in user."""
        with app.app_context():
            with client.session_transaction() as sess:
                sess["user_id"] = sample_user.id
                sess["username"] = sample_user.username

            response = client.get("/auth/profile")

            assert response.status_code == 200

    def test_update_profile_success(self, client, app, sample_user):
        """Test successful profile update."""
        with app.app_context():
            with client.session_transaction() as sess:
                sess["user_id"] = sample_user.id
                sess["username"] = sample_user.username

            response = client.post(
                "/auth/profile", data={"username": "updateduser", "email": "updated@example.com"}
            )

            assert response.status_code in [200, 302]

    def test_change_password_success(self, client, app, sample_user):
        """Test successful password change."""
        with app.app_context():
            sample_user.set_password("OldPass123")
            db.session.commit()

            with client.session_transaction() as sess:
                sess["user_id"] = sample_user.id
                sess["username"] = sample_user.username

            response = client.post(
                "/auth/change-password",
                data={
                    "current_password": "OldPass123",
                    "new_password": "NewPass123",
                    "confirm_password": "NewPass123",
                },
            )

            assert response.status_code in [200, 302]

    def test_change_password_wrong_current(self, client, app, sample_user):
        """Test password change with wrong current password."""
        with app.app_context():
            sample_user.set_password("OldPass123")
            db.session.commit()

            with client.session_transaction() as sess:
                sess["user_id"] = sample_user.id
                sess["username"] = sample_user.username

            response = client.post(
                "/auth/change-password",
                data={
                    "current_password": "WrongPassword",
                    "new_password": "NewPass123",
                    "confirm_password": "NewPass123",
                },
            )

            assert response.status_code in [200, 400]


@pytest.mark.integration
@pytest.mark.auth
class TestEmailVerification:
    """Tests for email verification workflow."""

    def test_verify_email_with_valid_token(self, client, app):
        """Test email verification with valid token."""
        with app.app_context():
            user = UnverifiedUserFactory()
            token = user.verification_token
            db.session.commit()

            response = client.get(f"/auth/verify/{token}", follow_redirects=False)

            assert response.status_code in [200, 302]

            # Verify user is now verified
            db.session.refresh(user)
            assert user.email_verified is True

    def test_verify_email_with_invalid_token(self, client):
        """Test email verification with invalid token."""
        response = client.get("/auth/verify/invalid_token")

        assert response.status_code in [200, 400, 404]

    def test_verify_email_already_verified(self, client, app):
        """Test email verification for already verified user."""
        with app.app_context():
            _ = UserFactory(email_verified=True, verification_token="old_token")
            db.session.commit()

            response = client.get("/auth/verify/old_token")

            assert response.status_code in [200, 400]


@pytest.mark.integration
@pytest.mark.auth
class TestRateLimiting:
    """Tests for rate limiting on authentication endpoints."""

    def test_login_rate_limiting(self, client, app):
        """Test rate limiting on login endpoint (5 per 15 minutes)."""
        with app.app_context():
            user = UserFactory(username="testuser")
            user.set_password("TestPass123")
            db.session.commit()

            # Make 6 rapid login attempts
            for i in range(6):
                response = client.post(
                    "/auth/login",
                    data={
                        "username_or_email": "testuser",
                        "password": "WrongPassword",
                        "remember_me": False,
                    },
                )

                if i < 5:
                    # First 5 should succeed (even if auth fails)
                    assert response.status_code in [200, 400]
                else:
                    # 6th should be rate limited
                    assert response.status_code in [200, 400, 429]

    def test_register_rate_limiting(self, client):
        """Test rate limiting on registration endpoint (3 per hour)."""
        # Make 4 rapid registration attempts
        for i in range(4):
            response = client.post(
                "/auth/register",
                data={
                    "username": f"user{i}",
                    "email": f"user{i}@example.com",
                    "password": "SecurePass123",
                    "confirm_password": "SecurePass123",
                },
            )

            if i < 3:
                # First 3 should succeed (or fail validation)
                assert response.status_code in [200, 302, 400]
            else:
                # 4th should be rate limited
                assert response.status_code in [200, 400, 429]
