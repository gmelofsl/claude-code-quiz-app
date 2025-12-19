"""
Authentication forms with comprehensive validation.

All forms include CSRF protection via Flask-WTF.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError, Regexp
)
from app.models.user import User


class RegistrationForm(FlaskForm):
    """User registration form with validation."""

    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters'),
        Regexp('^[A-Za-z0-9_]+$', message='Username must contain only letters, numbers, and underscores')
    ])

    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])

    submit = SubmitField('Register')

    def validate_username(self, username):
        """Check if username is already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        """Check if email is already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email or login.')

    def validate_password(self, password):
        """Validate password strength requirements."""
        pwd = password.data

        # Check for at least one uppercase letter
        if not any(c.isupper() for c in pwd):
            raise ValidationError('Password must contain at least one uppercase letter')

        # Check for at least one lowercase letter
        if not any(c.islower() for c in pwd):
            raise ValidationError('Password must contain at least one lowercase letter')

        # Check for at least one digit
        if not any(c.isdigit() for c in pwd):
            raise ValidationError('Password must contain at least one number')


class LoginForm(FlaskForm):
    """User login form."""

    username_or_email = StringField('Username or Email', validators=[
        DataRequired(message='Username or email is required'),
        Length(min=3, max=120, message='Invalid username or email length')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Login')


class ForgotPasswordForm(FlaskForm):
    """Forgot password form - request password reset."""

    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])

    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """Check if email exists in database."""
        user = User.query.filter_by(email=email.data).first()
        if not user:
            # Security: Don't reveal if email exists or not
            # But we still validate the form normally
            pass


class ResetPasswordForm(FlaskForm):
    """Reset password form - set new password with token."""

    password = PasswordField('New Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])

    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])

    submit = SubmitField('Reset Password')

    def validate_password(self, password):
        """Validate password strength requirements."""
        pwd = password.data

        # Check for at least one uppercase letter
        if not any(c.isupper() for c in pwd):
            raise ValidationError('Password must contain at least one uppercase letter')

        # Check for at least one lowercase letter
        if not any(c.islower() for c in pwd):
            raise ValidationError('Password must contain at least one lowercase letter')

        # Check for at least one digit
        if not any(c.isdigit() for c in pwd):
            raise ValidationError('Password must contain at least one number')


class ChangePasswordForm(FlaskForm):
    """Change password form - for logged-in users."""

    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required')
    ])

    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])

    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password'),
        EqualTo('new_password', message='Passwords must match')
    ])

    submit = SubmitField('Change Password')

    def validate_new_password(self, new_password):
        """Validate password strength requirements."""
        pwd = new_password.data

        # Check for at least one uppercase letter
        if not any(c.isupper() for c in pwd):
            raise ValidationError('Password must contain at least one uppercase letter')

        # Check for at least one lowercase letter
        if not any(c.islower() for c in pwd):
            raise ValidationError('Password must contain at least one lowercase letter')

        # Check for at least one digit
        if not any(c.isdigit() for c in pwd):
            raise ValidationError('Password must contain at least one number')


class UpdateProfileForm(FlaskForm):
    """Update user profile form."""

    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters'),
        Regexp('^[A-Za-z0-9_]+$', message='Username must contain only letters, numbers, and underscores')
    ])

    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ])

    submit = SubmitField('Update Profile')

    def __init__(self, original_username, original_email, *args, **kwargs):
        """Initialize form with current user data."""
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        """Check if username is already taken (if changed)."""
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        """Check if email is already registered (if changed)."""
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please use a different email.')
