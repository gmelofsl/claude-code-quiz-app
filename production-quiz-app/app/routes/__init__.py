"""
Routes package for the Quiz App.

Imports all blueprints for easy access.
"""

from app.routes.auth import auth_bp

__all__ = [
    'auth_bp',
]
