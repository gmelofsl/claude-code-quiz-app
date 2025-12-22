"""
Factory Boy factories for test data generation.

These factories use Factory Boy and Faker to generate realistic test data
for all models in the application.
"""

from datetime import datetime, timedelta

import factory
from factory import fuzzy

from app.extensions import db
from app.models import Attempt, Question, Quiz, User, UserAnswer


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Base factory with common configuration.

    All model factories inherit from this class.
    """

    class Meta:
        abstract = True
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    """
    Factory for creating User instances.

    Usage:
        user = UserFactory()
        user = UserFactory(username='custom_name')
        users = UserFactory.create_batch(5)
    """

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password_hash = factory.PostGenerationMethodCall("set_password", "TestPass123")
    is_active = True
    is_admin = False
    email_verified = True
    verification_token = None
    password_reset_token = None
    reset_token_expires = None
    failed_login_attempts = 0
    account_locked_until = None
    created_at = factory.LazyFunction(datetime.utcnow)
    last_active = factory.LazyFunction(datetime.utcnow)


class AdminUserFactory(UserFactory):
    """
    Factory for creating admin User instances.

    Usage:
        admin = AdminUserFactory()
    """

    username = factory.Sequence(lambda n: f"admin{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    is_admin = True


class UnverifiedUserFactory(UserFactory):
    """
    Factory for creating unverified User instances.

    Usage:
        user = UnverifiedUserFactory()
    """

    email_verified = False
    verification_token = factory.Faker("uuid4")


class LockedUserFactory(UserFactory):
    """
    Factory for creating locked User instances.

    Usage:
        user = LockedUserFactory()
    """

    failed_login_attempts = 5
    account_locked_until = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(minutes=15))


class QuizFactory(BaseFactory):
    """
    Factory for creating Quiz instances.

    Usage:
        quiz = QuizFactory()
        quiz = QuizFactory(category='Custom Category')
        quizzes = QuizFactory.create_batch(3)
    """

    class Meta:
        model = Quiz

    category = factory.Iterator(
        [
            "Agent Fundamentals",
            "Prompt Engineering",
            "Model Selection & Context Management",
            "Python Programming",
            "Web Development",
            "Data Science",
        ]
    )
    description = factory.LazyAttribute(lambda obj: f"Test your knowledge of {obj.category}")
    icon = factory.Iterator(["robot", "pencil", "target", "code", "web", "chart"])
    total_questions = 10
    is_active = True
    time_limit_minutes = None
    created_at = factory.LazyFunction(datetime.utcnow)


class TimedQuizFactory(QuizFactory):
    """
    Factory for creating timed Quiz instances.

    Usage:
        quiz = TimedQuizFactory()
        quiz = TimedQuizFactory(time_limit_minutes=30)
    """

    time_limit_minutes = 15


class QuestionFactory(BaseFactory):
    """
    Factory for creating Question instances.

    Usage:
        question = QuestionFactory(quiz=quiz)
        questions = QuestionFactory.create_batch(5, quiz=quiz)
    """

    class Meta:
        model = Question

    quiz = factory.SubFactory(QuizFactory)
    quiz_id = factory.LazyAttribute(lambda obj: obj.quiz.id)
    question = factory.Faker("sentence", nb_words=10)
    option_1 = factory.Faker("word")
    option_2 = factory.Faker("word")
    option_3 = factory.Faker("word")
    option_4 = factory.Faker("word")
    correct_answer = fuzzy.FuzzyChoice([0, 1, 2, 3])
    difficulty = fuzzy.FuzzyChoice(["easy", "medium", "hard"])
    explanation = factory.Faker("sentence", nb_words=15)
    order_index = factory.Sequence(lambda n: n)


class EasyQuestionFactory(QuestionFactory):
    """Factory for creating easy Question instances."""

    difficulty = "easy"


class MediumQuestionFactory(QuestionFactory):
    """Factory for creating medium Question instances."""

    difficulty = "medium"


class HardQuestionFactory(QuestionFactory):
    """Factory for creating hard Question instances."""

    difficulty = "hard"


class AttemptFactory(BaseFactory):
    """
    Factory for creating Attempt instances.

    Usage:
        attempt = AttemptFactory(user=user, quiz=quiz)
        attempt = AttemptFactory.create_completed(user=user, quiz=quiz)
    """

    class Meta:
        model = Attempt

    user = factory.SubFactory(UserFactory)
    user_id = factory.LazyAttribute(lambda obj: obj.user.id)
    quiz = factory.SubFactory(QuizFactory)
    quiz_id = factory.LazyAttribute(lambda obj: obj.quiz.id)
    score = None
    percentage = None
    time_taken = None
    started_at = factory.LazyFunction(datetime.utcnow)
    completed_at = None

    @classmethod
    def create_completed(cls, **kwargs):
        """
        Create a completed attempt with score and completion time.

        Args:
            **kwargs: Override default values

        Returns:
            Completed Attempt instance
        """
        # Default values for completed attempt
        if "score" not in kwargs:
            kwargs["score"] = fuzzy.FuzzyInteger(0, 10).fuzz()
        if "time_taken" not in kwargs:
            kwargs["time_taken"] = fuzzy.FuzzyInteger(60, 1800).fuzz()  # 1-30 mins

        attempt = cls(**kwargs)
        attempt.complete(score=kwargs["score"], time_taken=kwargs.get("time_taken"))

        return attempt

    @classmethod
    def create_in_progress(cls, **kwargs):
        """
        Create an in-progress attempt (not completed).

        Args:
            **kwargs: Override default values

        Returns:
            In-progress Attempt instance
        """
        kwargs["score"] = None
        kwargs["percentage"] = None
        kwargs["completed_at"] = None
        kwargs["time_taken"] = None

        return cls(**kwargs)


class CompletedAttemptFactory(AttemptFactory):
    """
    Factory for creating completed Attempt instances.

    Usage:
        attempt = CompletedAttemptFactory(user=user, quiz=quiz)
    """

    score = fuzzy.FuzzyInteger(0, 10)
    percentage = factory.LazyAttribute(lambda obj: (obj.score / 10) * 100)
    time_taken = fuzzy.FuzzyInteger(60, 1800)  # 1-30 minutes
    completed_at = factory.LazyFunction(datetime.utcnow)


class UserAnswerFactory(BaseFactory):
    """
    Factory for creating UserAnswer instances.

    Usage:
        answer = UserAnswerFactory(attempt=attempt, question=question)
        answer = UserAnswerFactory.create_correct(attempt=attempt, question=question)
    """

    class Meta:
        model = UserAnswer

    attempt = factory.SubFactory(AttemptFactory)
    attempt_id = factory.LazyAttribute(lambda obj: obj.attempt.id)
    question = factory.SubFactory(QuestionFactory)
    question_id = factory.LazyAttribute(lambda obj: obj.question.id)
    selected_answer = fuzzy.FuzzyChoice([0, 1, 2, 3])
    is_correct = factory.LazyAttribute(
        lambda obj: obj.selected_answer == obj.question.correct_answer
    )
    answered_at = factory.LazyFunction(datetime.utcnow)

    @classmethod
    def create_correct(cls, **kwargs):
        """
        Create a correct UserAnswer (selected_answer = correct_answer).

        Args:
            **kwargs: Override default values (must include question)

        Returns:
            Correct UserAnswer instance
        """
        question = kwargs.get("question")
        if not question:
            raise ValueError("question is required for create_correct")

        kwargs["selected_answer"] = question.correct_answer
        kwargs["is_correct"] = True

        return cls(**kwargs)

    @classmethod
    def create_incorrect(cls, **kwargs):
        """
        Create an incorrect UserAnswer (selected_answer != correct_answer).

        Args:
            **kwargs: Override default values (must include question)

        Returns:
            Incorrect UserAnswer instance
        """
        question = kwargs.get("question")
        if not question:
            raise ValueError("question is required for create_incorrect")

        # Select wrong answer
        wrong_answers = [i for i in range(4) if i != question.correct_answer]
        kwargs["selected_answer"] = wrong_answers[0]
        kwargs["is_correct"] = False

        return cls(**kwargs)


# Helper functions for common test data scenarios


def create_quiz_with_questions(num_questions=10, **quiz_kwargs):
    """
    Create a quiz with specified number of questions.

    Args:
        num_questions: Number of questions to create (default: 10)
        **quiz_kwargs: Additional quiz attributes

    Returns:
        Tuple of (quiz, questions_list)
    """
    quiz = QuizFactory(**quiz_kwargs)
    quiz.total_questions = num_questions
    db.session.commit()

    questions = QuestionFactory.create_batch(num_questions, quiz=quiz)

    return quiz, questions


def create_completed_quiz_attempt(user, quiz, score=None):
    """
    Create a fully completed quiz attempt with answers.

    Args:
        user: User taking the quiz
        quiz: Quiz being taken
        score: Score to achieve (default: random between 50-100%)

    Returns:
        Tuple of (attempt, answers_list)
    """
    # Get quiz questions
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    total = len(questions)

    # Determine score
    if score is None:
        score = fuzzy.FuzzyInteger(int(total * 0.5), total).fuzz()

    # Create attempt
    attempt = AttemptFactory.create_in_progress(user=user, quiz=quiz)

    # Create answers (correct up to score, incorrect after)
    answers = []
    for i, question in enumerate(questions):
        if i < score:
            answer = UserAnswerFactory.create_correct(attempt=attempt, question=question)
        else:
            answer = UserAnswerFactory.create_incorrect(attempt=attempt, question=question)
        answers.append(answer)

    # Complete attempt
    attempt.complete(score=score, time_taken=fuzzy.FuzzyInteger(60, 1800).fuzz())
    db.session.commit()

    return attempt, answers


def create_user_with_history(num_attempts=5):
    """
    Create a user with quiz attempt history.

    Args:
        num_attempts: Number of quiz attempts to create

    Returns:
        Tuple of (user, attempts_list)
    """
    user = UserFactory()
    quizzes = QuizFactory.create_batch(3)

    attempts = []
    for i in range(num_attempts):
        quiz = quizzes[i % len(quizzes)]
        _ = QuestionFactory.create_batch(10, quiz=quiz)  # Create questions for quiz
        quiz.total_questions = 10
        db.session.commit()

        attempt, _ = create_completed_quiz_attempt(user, quiz)
        attempts.append(attempt)

    return user, attempts
