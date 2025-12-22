"""
Attempt model for tracking quiz attempts and scores.
"""

from datetime import datetime

from app.extensions import db


class Attempt(db.Model):
    """
    Attempt model for tracking user quiz attempts.

    Records when a user starts and completes a quiz, along with their score.
    """

    __tablename__ = "attempts"

    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False, index=True)

    # Timing
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, index=True)
    time_taken = db.Column(db.Integer, nullable=True)  # Time taken in seconds

    # Scoring
    score = db.Column(db.Integer, nullable=True)  # Number of correct answers
    total_questions = db.Column(db.Integer, nullable=True)
    percentage = db.Column(db.Float, nullable=True)  # Score as percentage

    # Relationships
    user_answers = db.relationship(
        "UserAnswer", backref="attempt", lazy=True, cascade="all, delete-orphan"
    )

    # Indexes and constraints
    __table_args__ = (
        # Composite index for user-quiz queries
        db.Index("idx_attempt_user_quiz", "user_id", "quiz_id"),
        # Index for completed attempts filtering
        db.Index("idx_attempt_completed_at", "completed_at"),
        # Data validation constraints
        db.CheckConstraint(
            "score IS NULL OR (score >= 0 AND score <= total_questions)", name="check_score_valid"
        ),
        db.CheckConstraint(
            "percentage IS NULL OR (percentage >= 0 AND percentage <= 100)",
            name="check_percentage_valid",
        ),
        db.CheckConstraint(
            "time_taken IS NULL OR time_taken >= 0", name="check_time_taken_positive"
        ),
    )

    def __repr__(self):
        return f"<Attempt {self.id} by User {self.user_id} on Quiz {self.quiz_id}>"

    def is_completed(self):
        """
        Check if attempt is completed.

        Returns:
            bool: True if attempt has been completed
        """
        return self.completed_at is not None

    def complete(self, score, total_questions):
        """
        Mark attempt as completed and calculate score.

        Args:
            score: Number of correct answers
            total_questions: Total number of questions in quiz
        """
        self.completed_at = datetime.utcnow()
        self.score = score
        self.total_questions = total_questions
        self.percentage = round((score / total_questions) * 100, 2) if total_questions > 0 else 0

        # Calculate time taken
        if self.started_at:
            time_delta = self.completed_at - self.started_at
            self.time_taken = int(time_delta.total_seconds())

    def get_formatted_date(self):
        """
        Get formatted completion date.

        Returns:
            str: Formatted date or 'In Progress' if not completed
        """
        if self.completed_at:
            return self.completed_at.strftime("%Y-%m-%d %H:%M")
        return "In Progress"

    def get_formatted_duration(self):
        """
        Get formatted duration in minutes and seconds.

        Returns:
            str: Formatted duration (e.g., "5m 30s") or 'N/A' if not completed
        """
        if not self.time_taken:
            return "N/A"

        minutes = self.time_taken // 60
        seconds = self.time_taken % 60

        if minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"

    def get_performance_message(self):
        """
        Get motivational message based on performance.

        Returns:
            str: Performance message
        """
        if self.percentage is None:
            return ""

        if self.percentage >= 90:
            return "Outstanding! You're an expert!"
        elif self.percentage >= 75:
            return "Great job! Keep up the good work!"
        elif self.percentage >= 60:
            return "Good effort! Review the explanations to improve."
        elif self.percentage >= 50:
            return "Not bad! Study the topics and try again."
        else:
            return "Keep learning! Review the material and retake the quiz."

    def get_answers_by_correctness(self):
        """
        Get user answers grouped by correctness.

        Returns:
            dict: Dictionary with 'correct' and 'incorrect' answer lists
        """
        correct_answers = [a for a in self.user_answers if a.is_correct]
        incorrect_answers = [a for a in self.user_answers if not a.is_correct]

        return {"correct": correct_answers, "incorrect": incorrect_answers}

    def to_dict(self):
        """
        Convert attempt to dictionary format.

        Returns:
            dict: Attempt information
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quiz_id": self.quiz_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "score": self.score,
            "total_questions": self.total_questions,
            "percentage": self.percentage,
            "time_taken": self.time_taken,
            "is_completed": self.is_completed(),
        }
