"""
Unit tests for database models.

Tests model methods, properties, and relationships.
"""

from datetime import datetime, timedelta

import pytest

from app.extensions import db
from app.models import Attempt, Question, Quiz, User, UserAnswer
from tests.factories import (
    AttemptFactory,
    QuestionFactory,
    QuizFactory,
    UserAnswerFactory,
    UserFactory,
    create_completed_quiz_attempt,
    create_quiz_with_questions,
)


@pytest.mark.unit
@pytest.mark.models
class TestUserModel:
    """Tests for User model."""

    def test_create_user(self, app):
        """Test creating a basic user."""
        with app.app_context():
            user = UserFactory()

            assert user.id is not None
            assert user.username is not None
            assert user.email is not None
            assert user.is_active is True
            assert user.is_admin is False
            assert user.email_verified is True

    def test_set_password(self, app):
        """Test password hashing."""
        with app.app_context():
            user = UserFactory()
            user.set_password("NewPassword123")

            assert user.password_hash is not None
            assert user.password_hash != "NewPassword123"
            assert len(user.password_hash) > 20

    def test_check_password_correct(self, app):
        """Test checking correct password."""
        with app.app_context():
            user = UserFactory()
            user.set_password("TestPass123")
            db.session.commit()

            assert user.check_password("TestPass123") is True

    def test_check_password_incorrect(self, app):
        """Test checking incorrect password."""
        with app.app_context():
            user = UserFactory()
            user.set_password("TestPass123")
            db.session.commit()

            assert user.check_password("WrongPassword") is False

    def test_check_password_no_hash(self, app):
        """Test checking password when no hash exists."""
        with app.app_context():
            user = UserFactory.build(password_hash=None)
            db.session.add(user)
            db.session.commit()

            assert user.check_password("AnyPassword") is False

    def test_generate_verification_token(self, app):
        """Test generating email verification token."""
        with app.app_context():
            user = UserFactory()
            token = user.generate_verification_token()

            assert token is not None
            assert len(token) > 20
            assert user.verification_token == token

    def test_generate_reset_token(self, app):
        """Test generating password reset token."""
        with app.app_context():
            user = UserFactory()
            token = user.generate_reset_token()

            assert token is not None
            assert len(token) > 20
            assert user.password_reset_token == token
            assert user.reset_token_expires is not None
            assert user.reset_token_expires > datetime.utcnow()

    def test_verify_reset_token_valid(self, app):
        """Test verifying valid reset token."""
        with app.app_context():
            user = UserFactory()
            token = user.generate_reset_token()
            db.session.commit()

            assert user.verify_reset_token(token) is True

    def test_verify_reset_token_invalid(self, app):
        """Test verifying invalid reset token."""
        with app.app_context():
            user = UserFactory()
            user.generate_reset_token()
            db.session.commit()

            assert user.verify_reset_token("wrong_token") is False

    def test_verify_reset_token_expired(self, app):
        """Test verifying expired reset token."""
        with app.app_context():
            user = UserFactory()
            token = user.generate_reset_token()
            # Set expiration to past
            user.reset_token_expires = datetime.utcnow() - timedelta(hours=1)
            db.session.commit()

            assert user.verify_reset_token(token) is False

    def test_record_failed_login(self, app):
        """Test recording failed login attempt."""
        with app.app_context():
            user = UserFactory(failed_login_attempts=0)
            user.record_failed_login()

            assert user.failed_login_attempts == 1
            assert user.account_locked_until is None

    def test_record_failed_login_lockout(self, app):
        """Test account lockout after 5 failed attempts."""
        with app.app_context():
            user = UserFactory(failed_login_attempts=4)
            user.record_failed_login()

            assert user.failed_login_attempts == 5
            assert user.account_locked_until is not None
            assert user.account_locked_until > datetime.utcnow()

    def test_reset_failed_logins(self, app):
        """Test resetting failed login counter."""
        with app.app_context():
            user = UserFactory(
                failed_login_attempts=3,
                account_locked_until=datetime.utcnow() + timedelta(minutes=15),
            )
            user.reset_failed_logins()

            assert user.failed_login_attempts == 0
            assert user.account_locked_until is None

    def test_is_account_locked_true(self, app):
        """Test checking if account is locked (locked)."""
        with app.app_context():
            user = UserFactory(account_locked_until=datetime.utcnow() + timedelta(minutes=10))

            assert user.is_account_locked() is True

    def test_is_account_locked_false(self, app):
        """Test checking if account is locked (not locked)."""
        with app.app_context():
            user = UserFactory(account_locked_until=None)

            assert user.is_account_locked() is False

    def test_is_account_locked_expired(self, app):
        """Test checking if account is locked (lock expired)."""
        with app.app_context():
            user = UserFactory(account_locked_until=datetime.utcnow() - timedelta(minutes=10))

            assert user.is_account_locked() is False

    def test_update_last_active(self, app):
        """Test updating last active timestamp."""
        with app.app_context():
            old_time = datetime.utcnow() - timedelta(hours=1)
            user = UserFactory()
            user.last_active = old_time
            db.session.commit()

            user.update_last_active()
            db.session.commit()

            assert user.last_active > old_time

    def test_get_stats_no_attempts(self, app):
        """Test getting user stats with no attempts."""
        with app.app_context():
            user = UserFactory()
            stats = user.get_stats()

            assert stats["total_attempts"] == 0
            assert stats["average_score"] == 0
            assert stats["best_score"] == 0

    def test_get_stats_with_attempts(self, app):
        """Test getting user stats with completed attempts."""
        with app.app_context():
            user = UserFactory()
            quiz, questions = create_quiz_with_questions(num_questions=10)

            # Create 3 completed attempts
            for score in [7, 8, 9]:
                _ = AttemptFactory.create_completed(user=user, quiz=quiz, score=score)

            stats = user.get_stats()

            assert stats["total_attempts"] == 3
            assert stats["average_score"] == 80.0  # (70 + 80 + 90) / 3
            assert stats["best_score"] == 90.0

    def test_user_relationship_with_attempts(self, app):
        """Test User -> Attempt relationship."""
        with app.app_context():
            user = UserFactory()
            quiz = QuizFactory()
            attempt1 = AttemptFactory(user=user, quiz=quiz)
            attempt2 = AttemptFactory(user=user, quiz=quiz)
            db.session.commit()

            assert len(user.attempts) == 2
            assert attempt1 in user.attempts
            assert attempt2 in user.attempts


@pytest.mark.unit
@pytest.mark.models
class TestQuizModel:
    """Tests for Quiz model."""

    def test_create_quiz(self, app):
        """Test creating a basic quiz."""
        with app.app_context():
            quiz = QuizFactory()

            assert quiz.id is not None
            assert quiz.category is not None
            assert quiz.description is not None
            assert quiz.is_active is True

    def test_quiz_relationship_with_questions(self, app):
        """Test Quiz -> Question relationship."""
        with app.app_context():
            quiz, questions = create_quiz_with_questions(num_questions=5)

            assert len(quiz.questions) == 5
            assert all(q.quiz_id == quiz.id for q in questions)

    def test_get_average_score_no_attempts(self, app):
        """Test getting average score with no attempts."""
        with app.app_context():
            quiz = QuizFactory()

            assert quiz.get_average_score() == 0

    def test_get_average_score_with_attempts(self, app):
        """Test getting average score with completed attempts."""
        with app.app_context():
            quiz, questions = create_quiz_with_questions(num_questions=10)
            user = UserFactory()

            # Create 3 completed attempts
            for score in [6, 8, 10]:
                AttemptFactory.create_completed(user=user, quiz=quiz, score=score)

            avg_score = quiz.get_average_score()
            assert avg_score == 80.0  # (60 + 80 + 100) / 3

    def test_get_completion_rate_no_attempts(self, app):
        """Test getting completion rate with no attempts."""
        with app.app_context():
            quiz = QuizFactory()

            assert quiz.get_completion_rate() == 0

    def test_get_completion_rate_all_completed(self, app):
        """Test getting completion rate when all attempts completed."""
        with app.app_context():
            quiz, questions = create_quiz_with_questions(num_questions=10)
            user = UserFactory()

            # Create 3 completed attempts
            for i in range(3):
                AttemptFactory.create_completed(user=user, quiz=quiz, score=5)

            completion_rate = quiz.get_completion_rate()
            assert completion_rate == 100.0

    def test_get_completion_rate_partial(self, app):
        """Test getting completion rate with partial completion."""
        with app.app_context():
            quiz, questions = create_quiz_with_questions(num_questions=10)
            user = UserFactory()

            # Create 2 completed, 1 in-progress
            AttemptFactory.create_completed(user=user, quiz=quiz, score=5)
            AttemptFactory.create_completed(user=user, quiz=quiz, score=7)
            AttemptFactory.create_in_progress(user=user, quiz=quiz)

            completion_rate = quiz.get_completion_rate()
            assert completion_rate == pytest.approx(66.67, rel=0.01)

    def test_to_dict(self, app):
        """Test converting quiz to dictionary."""
        with app.app_context():
            quiz = QuizFactory()
            quiz_dict = quiz.to_dict()

            assert quiz_dict["id"] == quiz.id
            assert quiz_dict["category"] == quiz.category
            assert quiz_dict["description"] == quiz.description
            assert quiz_dict["total_questions"] == quiz.total_questions
            assert "created_at" in quiz_dict


@pytest.mark.unit
@pytest.mark.models
class TestQuestionModel:
    """Tests for Question model."""

    def test_create_question(self, app):
        """Test creating a basic question."""
        with app.app_context():
            question = QuestionFactory()

            assert question.id is not None
            assert question.question is not None
            assert question.correct_answer in [0, 1, 2, 3]
            assert question.difficulty in ["easy", "medium", "hard"]

    def test_get_correct_option_text(self, app):
        """Test getting correct option text."""
        with app.app_context():
            question = QuestionFactory(
                option_1="A", option_2="B", option_3="C", option_4="D", correct_answer=2
            )

            assert question.get_correct_option_text() == "C"

    def test_check_answer_correct(self, app):
        """Test checking correct answer."""
        with app.app_context():
            question = QuestionFactory(correct_answer=1)

            assert question.check_answer(1) is True

    def test_check_answer_incorrect(self, app):
        """Test checking incorrect answer."""
        with app.app_context():
            question = QuestionFactory(correct_answer=1)

            assert question.check_answer(2) is False

    def test_get_difficulty_weight_easy(self, app):
        """Test difficulty weight for easy questions."""
        with app.app_context():
            question = QuestionFactory(difficulty="easy")

            assert question.get_difficulty_weight() == 1

    def test_get_difficulty_weight_medium(self, app):
        """Test difficulty weight for medium questions."""
        with app.app_context():
            question = QuestionFactory(difficulty="medium")

            assert question.get_difficulty_weight() == 2

    def test_get_difficulty_weight_hard(self, app):
        """Test difficulty weight for hard questions."""
        with app.app_context():
            question = QuestionFactory(difficulty="hard")

            assert question.get_difficulty_weight() == 3

    def test_to_dict(self, app):
        """Test converting question to dictionary."""
        with app.app_context():
            question = QuestionFactory()
            question_dict = question.to_dict()

            assert question_dict["id"] == question.id
            assert question_dict["question"] == question.question
            assert "options" in question_dict
            assert len(question_dict["options"]) == 4


@pytest.mark.unit
@pytest.mark.models
class TestAttemptModel:
    """Tests for Attempt model."""

    def test_create_attempt(self, app):
        """Test creating an in-progress attempt."""
        with app.app_context():
            attempt = AttemptFactory.create_in_progress()

            assert attempt.id is not None
            assert attempt.score is None
            assert attempt.percentage is None
            assert attempt.completed_at is None

    def test_complete_attempt(self, app):
        """Test completing an attempt."""
        with app.app_context():
            quiz, questions = create_quiz_with_questions(num_questions=10)
            user = UserFactory()
            attempt = AttemptFactory.create_in_progress(user=user, quiz=quiz)

            attempt.complete(score=7, time_taken=600)
            db.session.commit()

            assert attempt.score == 7
            assert attempt.percentage == 70.0
            assert attempt.time_taken == 600
            assert attempt.completed_at is not None

    def test_get_formatted_duration_completed(self, app):
        """Test formatted duration for completed attempt."""
        with app.app_context():
            attempt = AttemptFactory.create_completed(time_taken=125)

            assert attempt.get_formatted_duration() == "2m 5s"

    def test_get_formatted_duration_in_progress(self, app):
        """Test formatted duration for in-progress attempt."""
        with app.app_context():
            attempt = AttemptFactory.create_in_progress()

            assert attempt.get_formatted_duration() == "In Progress"

    def test_get_formatted_date_completed(self, app):
        """Test formatted date for completed attempt."""
        with app.app_context():
            attempt = AttemptFactory.create_completed()

            formatted_date = attempt.get_formatted_date()
            assert formatted_date != "In Progress"
            assert len(formatted_date) > 0

    def test_get_formatted_date_in_progress(self, app):
        """Test formatted date for in-progress attempt."""
        with app.app_context():
            attempt = AttemptFactory.create_in_progress()

            assert attempt.get_formatted_date() == "In Progress"

    def test_get_performance_message_excellent(self, app):
        """Test performance message for excellent score (90%+)."""
        with app.app_context():
            attempt = AttemptFactory.create_completed(score=9)

            message = attempt.get_performance_message()
            assert "Excellent" in message or "Outstanding" in message

    def test_get_performance_message_good(self, app):
        """Test performance message for good score (70-89%)."""
        with app.app_context():
            attempt = AttemptFactory.create_completed(score=7)

            message = attempt.get_performance_message()
            assert "Good" in message or "Well done" in message

    def test_get_performance_message_pass(self, app):
        """Test performance message for passing score (50-69%)."""
        with app.app_context():
            attempt = AttemptFactory.create_completed(score=5)

            message = attempt.get_performance_message()
            assert "Pass" in message or "passed" in message.lower()

    def test_get_performance_message_fail(self, app):
        """Test performance message for failing score (<50%)."""
        with app.app_context():
            attempt = AttemptFactory.create_completed(score=3)

            message = attempt.get_performance_message()
            assert "study" in message.lower() or "review" in message.lower()


@pytest.mark.unit
@pytest.mark.models
class TestUserAnswerModel:
    """Tests for UserAnswer model."""

    def test_create_user_answer(self, app):
        """Test creating a user answer."""
        with app.app_context():
            answer = UserAnswerFactory()

            assert answer.id is not None
            assert answer.selected_answer in [0, 1, 2, 3]
            assert isinstance(answer.is_correct, bool)

    def test_get_selected_option_text(self, app):
        """Test getting selected option text."""
        with app.app_context():
            question = QuestionFactory(option_1="A", option_2="B", option_3="C", option_4="D")
            answer = UserAnswerFactory(question=question, selected_answer=1)

            assert answer.get_selected_option_text() == "B"

    def test_get_correct_option_text(self, app):
        """Test getting correct option text."""
        with app.app_context():
            question = QuestionFactory(
                option_1="A", option_2="B", option_3="C", option_4="D", correct_answer=2
            )
            answer = UserAnswerFactory(question=question)

            assert answer.get_correct_option_text() == "C"

    def test_create_correct_answer(self, app):
        """Test factory method for correct answer."""
        with app.app_context():
            question = QuestionFactory(correct_answer=1)
            attempt = AttemptFactory.create_in_progress()
            answer = UserAnswerFactory.create_correct(question=question, attempt=attempt)

            assert answer.selected_answer == question.correct_answer
            assert answer.is_correct is True

    def test_create_incorrect_answer(self, app):
        """Test factory method for incorrect answer."""
        with app.app_context():
            question = QuestionFactory(correct_answer=1)
            attempt = AttemptFactory.create_in_progress()
            answer = UserAnswerFactory.create_incorrect(question=question, attempt=attempt)

            assert answer.selected_answer != question.correct_answer
            assert answer.is_correct is False
