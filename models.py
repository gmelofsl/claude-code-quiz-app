from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    attempts = db.relationship('Attempt', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def get_stats(self):
        """Get user statistics"""
        total_attempts = len(self.attempts)
        if total_attempts == 0:
            return {
                'total_attempts': 0,
                'avg_score': 0,
                'best_score': 0
            }

        completed_attempts = [a for a in self.attempts if a.completed_at is not None]
        if not completed_attempts:
            return {
                'total_attempts': 0,
                'avg_score': 0,
                'best_score': 0
            }

        percentages = [a.percentage for a in completed_attempts]
        return {
            'total_attempts': len(completed_attempts),
            'avg_score': round(sum(percentages) / len(percentages), 1),
            'best_score': round(max(percentages), 1)
        }


class Quiz(db.Model):
    """Quiz model for storing quiz categories"""
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('Attempt', backref='quiz', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Quiz {self.title}>'

    def get_question_count(self):
        """Get total number of questions in this quiz"""
        return len(self.questions)


class Question(db.Model):
    """Question model for storing quiz questions"""
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_1 = db.Column(db.String(500), nullable=False)
    option_2 = db.Column(db.String(500), nullable=False)
    option_3 = db.Column(db.String(500), nullable=False)
    option_4 = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)  # 0-3 index
    explanation = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    order_index = db.Column(db.Integer)

    # Relationships
    user_answers = db.relationship('UserAnswer', backref='question', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:50]}...>'

    def get_options_list(self):
        """Get options as a list"""
        return [self.option_1, self.option_2, self.option_3, self.option_4]

    def to_dict(self):
        """Convert question to dictionary format (compatible with session storage)"""
        return {
            'id': self.id,
            'question': self.question_text,
            'options': self.get_options_list(),
            'correct': self.correct_answer,
            'explanation': self.explanation,
            'difficulty': self.difficulty
        }


class Attempt(db.Model):
    """Attempt model for tracking quiz attempts"""
    __tablename__ = 'attempts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    percentage = db.Column(db.Float)

    # Relationships
    user_answers = db.relationship('UserAnswer', backref='attempt', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Attempt {self.id} by User {self.user_id} on Quiz {self.quiz_id}>'

    def is_completed(self):
        """Check if attempt is completed"""
        return self.completed_at is not None

    def get_formatted_date(self):
        """Get formatted completion date"""
        if self.completed_at:
            return self.completed_at.strftime('%Y-%m-%d %H:%M')
        return 'In Progress'


class UserAnswer(db.Model):
    """UserAnswer model for storing individual answers"""
    __tablename__ = 'user_answers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_answer = db.Column(db.Integer, nullable=False)  # 0-3 index
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserAnswer {self.id}: {"Correct" if self.is_correct else "Incorrect"}>'
