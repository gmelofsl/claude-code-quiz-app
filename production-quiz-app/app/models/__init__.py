"""
Models package for the Quiz App.

Imports all database models for easy access.
"""

from app.models.user import User
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.attempt import Attempt
from app.models.user_answer import UserAnswer

__all__ = [
    'User',
    'Quiz',
    'Question',
    'Attempt',
    'UserAnswer',
]
