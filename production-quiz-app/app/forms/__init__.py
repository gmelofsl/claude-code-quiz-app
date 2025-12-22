"""
Forms package for the Quiz App.

Imports all form classes for easy access.
"""

from app.forms.auth_forms import (
    ChangePasswordForm,
    ForgotPasswordForm,
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
    UpdateProfileForm,
)

__all__ = [
    "RegistrationForm",
    "LoginForm",
    "ForgotPasswordForm",
    "ResetPasswordForm",
    "ChangePasswordForm",
    "UpdateProfileForm",
]
