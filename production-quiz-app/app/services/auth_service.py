"""
Authentication service with business logic.

Handles user registration, login, password reset, email verification, etc.
"""

from datetime import datetime
from flask import current_app
from app.extensions import db
from app.models.user import User


class AuthService:
    """Authentication service for user management."""

    @staticmethod
    def register_user(username, email, password):
        """
        Register a new user.

        Args:
            username: Desired username
            email: User's email address
            password: Plain text password (will be hashed)

        Returns:
            tuple: (user, error_message)
                user: User object if successful, None if failed
                error_message: None if successful, error string if failed
        """
        try:
            # Check if username already exists
            if User.query.filter_by(username=username).first():
                return None, 'Username already taken'

            # Check if email already exists
            if User.query.filter_by(email=email).first():
                return None, 'Email already registered'

            # Create new user
            user = User(
                username=username,
                email=email,
                is_active=True,
                is_admin=False,
                email_verified=False
            )

            # Set password (hashed)
            user.set_password(password)

            # Generate email verification token
            user.generate_verification_token()

            # Save to database
            db.session.add(user)
            db.session.commit()

            current_app.logger.info(f'New user registered: {username}')

            return user, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Registration error: {e}')
            return None, 'Registration failed. Please try again.'

    @staticmethod
    def authenticate_user(username_or_email, password):
        """
        Authenticate user by username/email and password.

        Args:
            username_or_email: Username or email address
            password: Plain text password

        Returns:
            tuple: (user, error_message)
                user: User object if successful, None if failed
                error_message: None if successful, error string if failed
        """
        try:
            # Try to find user by username or email
            user = User.query.filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()

            # User not found
            if not user:
                return None, 'Invalid username/email or password'

            # Check if account is locked
            if user.is_account_locked():
                return None, 'Account temporarily locked due to multiple failed login attempts. Please try again later.'

            # Check if account is active
            if not user.is_active:
                return None, 'Account is deactivated. Please contact support.'

            # Verify password
            if not user.check_password(password):
                # Record failed login attempt
                user.record_failed_login()
                db.session.commit()
                return None, 'Invalid username/email or password'

            # Successful login - reset failed attempts
            user.reset_failed_logins()
            user.update_last_active()
            db.session.commit()

            current_app.logger.info(f'User logged in: {user.username}')

            return user, None

        except Exception as e:
            current_app.logger.error(f'Authentication error: {e}')
            return None, 'Login failed. Please try again.'

    @staticmethod
    def verify_email(token):
        """
        Verify user's email with verification token.

        Args:
            token: Email verification token

        Returns:
            tuple: (success, message)
                success: True if successful, False if failed
                message: Success or error message
        """
        try:
            # Find user by verification token
            user = User.query.filter_by(verification_token=token).first()

            if not user:
                return False, 'Invalid or expired verification token'

            # Mark email as verified
            user.verify_email()
            db.session.commit()

            current_app.logger.info(f'Email verified for user: {user.username}')

            return True, 'Email verified successfully! You can now log in.'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Email verification error: {e}')
            return False, 'Verification failed. Please try again.'

    @staticmethod
    def request_password_reset(email):
        """
        Request password reset for user.

        Args:
            email: User's email address

        Returns:
            tuple: (user, error_message)
                user: User object if found, None if not found
                error_message: None if successful, error string if failed

        Note: For security, we don't reveal if email exists or not in the return value.
              The calling code should always show success message.
        """
        try:
            # Find user by email
            user = User.query.filter_by(email=email).first()

            if not user:
                # Security: Don't reveal if email exists
                # Just return None silently
                return None, None

            # Generate reset token
            user.generate_reset_token(expires_in=3600)  # 1 hour expiration
            db.session.commit()

            current_app.logger.info(f'Password reset requested for: {user.username}')

            return user, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Password reset request error: {e}')
            return None, 'Failed to process password reset request'

    @staticmethod
    def reset_password(token, new_password):
        """
        Reset user password with reset token.

        Args:
            token: Password reset token
            new_password: New plain text password (will be hashed)

        Returns:
            tuple: (success, message)
                success: True if successful, False if failed
                message: Success or error message
        """
        try:
            # Find user by reset token
            user = User.query.filter_by(password_reset_token=token).first()

            if not user:
                return False, 'Invalid or expired reset token'

            # Verify token is not expired
            if not user.verify_reset_token(token):
                return False, 'Reset token has expired. Please request a new one.'

            # Set new password
            user.set_password(new_password)
            user.clear_reset_token()
            db.session.commit()

            current_app.logger.info(f'Password reset for user: {user.username}')

            return True, 'Password reset successfully! You can now log in with your new password.'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Password reset error: {e}')
            return False, 'Password reset failed. Please try again.'

    @staticmethod
    def change_password(user, current_password, new_password):
        """
        Change password for logged-in user.

        Args:
            user: User object
            current_password: Current plain text password
            new_password: New plain text password (will be hashed)

        Returns:
            tuple: (success, message)
                success: True if successful, False if failed
                message: Success or error message
        """
        try:
            # Verify current password
            if not user.check_password(current_password):
                return False, 'Current password is incorrect'

            # Set new password
            user.set_password(new_password)
            db.session.commit()

            current_app.logger.info(f'Password changed for user: {user.username}')

            return True, 'Password changed successfully!'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Password change error: {e}')
            return False, 'Password change failed. Please try again.'

    @staticmethod
    def update_profile(user, username, email):
        """
        Update user profile information.

        Args:
            user: User object
            username: New username
            email: New email

        Returns:
            tuple: (success, message)
                success: True if successful, False if failed
                message: Success or error message
        """
        try:
            # Check if username changed and is available
            if username != user.username:
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    return False, 'Username already taken'
                user.username = username

            # Check if email changed and is available
            email_changed = False
            if email != user.email:
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    return False, 'Email already registered'
                user.email = email
                user.email_verified = False  # Require re-verification
                user.generate_verification_token()
                email_changed = True

            db.session.commit()

            current_app.logger.info(f'Profile updated for user: {user.username}')

            if email_changed:
                return True, 'Profile updated successfully! Please verify your new email address.'
            else:
                return True, 'Profile updated successfully!'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Profile update error: {e}')
            return False, 'Profile update failed. Please try again.'

    @staticmethod
    def send_verification_email(user):
        """
        Send email verification email (placeholder for actual email sending).

        Args:
            user: User object with verification_token

        Returns:
            bool: True if email sent successfully

        Note: This is a placeholder. In production, integrate with email service
              (SendGrid, AWS SES, etc.)
        """
        # TODO: Implement actual email sending
        # For now, just log the verification URL
        verification_url = f'/auth/verify/{user.verification_token}'
        current_app.logger.info(f'Verification URL for {user.username}: {verification_url}')

        # In production, send email here
        # Example:
        # from flask_mail import Message
        # msg = Message('Verify Your Email',
        #               recipients=[user.email])
        # msg.body = f'Click to verify: {verification_url}'
        # mail.send(msg)

        return True

    @staticmethod
    def send_password_reset_email(user):
        """
        Send password reset email (placeholder for actual email sending).

        Args:
            user: User object with password_reset_token

        Returns:
            bool: True if email sent successfully

        Note: This is a placeholder. In production, integrate with email service.
        """
        # TODO: Implement actual email sending
        # For now, just log the reset URL
        reset_url = f'/auth/reset-password/{user.password_reset_token}'
        current_app.logger.info(f'Password reset URL for {user.username}: {reset_url}')

        # In production, send email here

        return True
