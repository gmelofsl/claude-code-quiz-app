"""
UserAnswer model for storing individual question answers.
"""

from datetime import datetime

from app.extensions import db


class UserAnswer(db.Model):
    """
    UserAnswer model for storing individual answers to questions.

    Each record represents one question answered in one attempt.
    """

    __tablename__ = "user_answers"

    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    attempt_id = db.Column(db.Integer, db.ForeignKey("attempts.id"), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False, index=True)

    # Answer data
    selected_answer = db.Column(db.Integer, nullable=True)  # 0-3 index, NULL if unanswered/skipped
    is_correct = db.Column(db.Boolean, nullable=False)

    # Timestamp
    answered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Indexes and constraints
    __table_args__ = (
        # Indexes for query performance
        db.Index("idx_user_answer_attempt_id", "attempt_id"),
        db.Index("idx_user_answer_question_id", "question_id"),
        # Unique constraint to prevent duplicate answers
        db.UniqueConstraint("attempt_id", "question_id", name="uq_attempt_question"),
        # Data validation constraint
        db.CheckConstraint(
            "selected_answer IS NULL OR (selected_answer >= 0 AND selected_answer <= 3)",
            name="check_selected_answer_range",
        ),
    )

    def __repr__(self):
        return f'<UserAnswer {self.id}: {"Correct" if self.is_correct else "Incorrect"}>'

    def get_selected_option_text(self):
        """
        Get the text of the selected answer option.

        Returns:
            str: Text of the selected answer or 'No answer' if not answered
        """
        if self.selected_answer is None:
            return "No answer"

        if self.question:
            options = self.question.get_options_list()
            if 0 <= self.selected_answer < len(options):
                return options[self.selected_answer]

        return f"Option {self.selected_answer + 1}"

    def get_correct_option_text(self):
        """
        Get the text of the correct answer option.

        Returns:
            str: Text of the correct answer
        """
        if self.question:
            return self.question.get_correct_option_text()
        return "Unknown"

    def to_dict(self):
        """
        Convert user answer to dictionary format.

        Returns:
            dict: User answer information
        """
        return {
            "id": self.id,
            "attempt_id": self.attempt_id,
            "question_id": self.question_id,
            "selected_answer": self.selected_answer,
            "is_correct": self.is_correct,
            "answered_at": self.answered_at.isoformat() if self.answered_at else None,
        }
