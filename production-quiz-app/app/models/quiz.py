"""
Quiz model for managing quiz categories and metadata.
"""

from datetime import datetime
from app.extensions import db


class Quiz(db.Model):
    """
    Quiz model for storing quiz categories and information.

    Each quiz represents a category (e.g., "Agent Fundamentals", "Prompt Engineering")
    and contains multiple questions.
    """
    __tablename__ = 'quizzes'

    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Quiz information
    category = db.Column(db.String(100), nullable=False, unique=True)  # Unique category name
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(10), nullable=True)  # Emoji or icon identifier

    # Metadata
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # For enabling/disabling quizzes
    time_limit_minutes = db.Column(db.Integer, nullable=True)  # Optional time limit for timed quizzes

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('Attempt', backref='quiz', lazy=True, cascade='all, delete-orphan')

    # Indexes and constraints
    __table_args__ = (
        db.Index('idx_quiz_category', 'category'),
        db.UniqueConstraint('category', name='uq_quiz_category'),
    )

    def __repr__(self):
        return f'<Quiz {self.title}>'

    def get_question_count(self):
        """
        Get total number of questions in this quiz.

        Returns:
            int: Number of questions
        """
        return len(self.questions)

    def get_average_score(self):
        """
        Get average score across all completed attempts for this quiz.

        Returns:
            float: Average percentage score, or 0 if no completed attempts
        """
        completed_attempts = [a for a in self.attempts if a.completed_at is not None]
        if not completed_attempts:
            return 0.0

        total_percentage = sum(a.percentage for a in completed_attempts)
        return round(total_percentage / len(completed_attempts), 1)

    def get_completion_rate(self):
        """
        Get percentage of attempts that were completed vs started.

        Returns:
            float: Completion rate percentage
        """
        if not self.attempts:
            return 0.0

        completed = sum(1 for a in self.attempts if a.completed_at is not None)
        return round((completed / len(self.attempts)) * 100, 1)

    def to_dict(self):
        """
        Convert quiz to dictionary format.

        Returns:
            dict: Quiz information
        """
        return {
            'id': self.id,
            'category': self.category,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'question_count': self.get_question_count(),
            'is_active': self.is_active,
            'time_limit_minutes': self.time_limit_minutes,
        }
