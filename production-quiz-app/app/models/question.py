"""
Question model for storing quiz questions and answers.
"""

from app.extensions import db


class Question(db.Model):
    """
    Question model for storing quiz questions with multiple choice answers.

    Each question belongs to a quiz and has 4 options with one correct answer.
    """

    __tablename__ = "questions"

    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign key
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False, index=True)

    # Question content
    question_text = db.Column(db.Text, nullable=False)

    # Answer options (4 options)
    option_1 = db.Column(db.String(500), nullable=False)
    option_2 = db.Column(db.String(500), nullable=False)
    option_3 = db.Column(db.String(500), nullable=False)
    option_4 = db.Column(db.String(500), nullable=False)

    # Correct answer (0-3 index corresponding to option_1 through option_4)
    correct_answer = db.Column(db.Integer, nullable=False)

    # Additional information
    explanation = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # 'easy', 'medium', or 'hard'
    order_index = db.Column(db.Integer, nullable=True)  # Order within quiz

    # Relationships
    user_answers = db.relationship(
        "UserAnswer", backref="question", lazy=True, cascade="all, delete-orphan"
    )

    # Indexes and constraints
    __table_args__ = (
        # Indexes for query performance
        db.Index("idx_question_quiz_id", "quiz_id"),
        db.Index("idx_question_difficulty", "difficulty"),
        db.Index("idx_question_quiz_difficulty", "quiz_id", "difficulty"),  # Composite index
        # Data validation constraints
        db.CheckConstraint(
            "correct_answer >= 0 AND correct_answer <= 3", name="check_correct_answer_range"
        ),
        db.CheckConstraint(
            "difficulty IN ('easy', 'medium', 'hard')", name="check_difficulty_enum"
        ),
    )

    def __repr__(self):
        return f"<Question {self.id}: {self.question_text[:50]}...>"

    def get_options_list(self):
        """
        Get answer options as a list.

        Returns:
            list: List of 4 answer options
        """
        return [self.option_1, self.option_2, self.option_3, self.option_4]

    def get_correct_option_text(self):
        """
        Get the text of the correct answer option.

        Returns:
            str: Text of the correct answer
        """
        options = self.get_options_list()
        return options[self.correct_answer]

    def to_dict(self):
        """
        Convert question to dictionary format (compatible with session storage).

        Returns:
            dict: Question data including id, text, options, correct answer, etc.
        """
        return {
            "id": self.id,
            "question": self.question_text,
            "options": self.get_options_list(),
            "correct": self.correct_answer,
            "explanation": self.explanation,
            "difficulty": self.difficulty,
        }

    def check_answer(self, selected_option):
        """
        Check if the selected option is correct.

        Args:
            selected_option: Index of selected option (0-3)

        Returns:
            bool: True if answer is correct
        """
        return selected_option == self.correct_answer

    def get_difficulty_weight(self):
        """
        Get point weight based on difficulty level.

        Returns:
            int: Points for this question (1=easy, 2=medium, 3=hard)
        """
        weights = {"easy": 1, "medium": 2, "hard": 3}
        return weights.get(self.difficulty, 1)
