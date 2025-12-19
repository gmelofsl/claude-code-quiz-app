"""
Pytest configuration and fixtures for Production Quiz App.

This module provides reusable test fixtures for the entire test suite.
"""

import os
import pytest
from flask import session
from app import create_app
from app.extensions import db
from app.models import User, Quiz, Question, Attempt, UserAnswer


@pytest.fixture(scope='session')
def app():
    """
    Create and configure a Flask application for testing.

    Uses testing configuration with in-memory SQLite database.
    Scope: session (created once per test session)
    """
    # Set testing environment
    os.environ['FLASK_ENV'] = 'testing'

    # Create app with testing config
    app = create_app('testing')

    # Establish application context
    with app.app_context():
        # Create all database tables
        db.create_all()

        yield app

        # Cleanup: drop all tables
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """
    Create a Flask test client.

    Scope: function (new client for each test)
    """
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """
    Create a Flask CLI test runner.

    Scope: function (new runner for each test)
    """
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_session(app):
    """
    Create a database session for testing with transaction rollback.

    Each test gets a clean database state through transaction rollback.
    Scope: function (new session for each test)
    """
    with app.app_context():
        # Begin a nested transaction
        connection = db.engine.connect()
        transaction = connection.begin()

        # Bind session to connection
        session_options = dict(bind=connection, binds={})
        sess = db.create_scoped_session(options=session_options)
        db.session = sess

        yield sess

        # Rollback transaction (undo all changes)
        sess.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope='function')
def sample_user(app):
    """
    Create a sample verified user for testing.

    Returns a User object with:
    - username: testuser
    - email: testuser@example.com
    - password: TestPass123
    - email_verified: True
    - is_active: True
    """
    with app.app_context():
        user = User(
            username='testuser',
            email='testuser@example.com',
            is_active=True,
            email_verified=True
        )
        user.set_password('TestPass123')
        db.session.add(user)
        db.session.commit()

        # Refresh to get ID and relationships
        db.session.refresh(user)

        yield user

        # Cleanup: delete user and cascade to attempts/answers
        db.session.delete(user)
        db.session.commit()


@pytest.fixture(scope='function')
def sample_admin_user(app):
    """
    Create a sample admin user for testing.

    Returns a User object with admin privileges.
    """
    with app.app_context():
        user = User(
            username='adminuser',
            email='admin@example.com',
            is_active=True,
            is_admin=True,
            email_verified=True
        )
        user.set_password('AdminPass123')
        db.session.add(user)
        db.session.commit()

        db.session.refresh(user)

        yield user

        db.session.delete(user)
        db.session.commit()


@pytest.fixture(scope='function')
def sample_quiz(app):
    """
    Create a sample quiz with questions for testing.

    Returns a Quiz object with 5 questions (mixed difficulty).
    """
    with app.app_context():
        # Create quiz
        quiz = Quiz(
            category='Test Category',
            description='A test quiz for testing purposes',
            icon='test-icon',
            total_questions=5,
            is_active=True
        )
        db.session.add(quiz)
        db.session.flush()  # Get quiz ID without committing

        # Create questions
        questions_data = [
            {
                'question': 'What is 2 + 2?',
                'options': ['3', '4', '5', '6'],
                'correct': 1,
                'difficulty': 'easy',
                'explanation': 'Basic arithmetic: 2 + 2 = 4'
            },
            {
                'question': 'What is the capital of France?',
                'options': ['London', 'Berlin', 'Paris', 'Madrid'],
                'correct': 2,
                'difficulty': 'easy',
                'explanation': 'Paris is the capital of France'
            },
            {
                'question': 'What is 15 * 8?',
                'options': ['110', '115', '120', '125'],
                'correct': 2,
                'difficulty': 'medium',
                'explanation': '15 * 8 = 120'
            },
            {
                'question': 'What is the square root of 144?',
                'options': ['10', '11', '12', '13'],
                'correct': 2,
                'difficulty': 'medium',
                'explanation': 'The square root of 144 is 12'
            },
            {
                'question': 'What is the derivative of x^2?',
                'options': ['x', '2x', 'x^2', '2'],
                'correct': 1,
                'difficulty': 'hard',
                'explanation': 'The derivative of x^2 is 2x'
            }
        ]

        for i, q_data in enumerate(questions_data):
            question = Question(
                quiz_id=quiz.id,
                question=q_data['question'],
                option_1=q_data['options'][0],
                option_2=q_data['options'][1],
                option_3=q_data['options'][2],
                option_4=q_data['options'][3],
                correct_answer=q_data['correct'],
                difficulty=q_data['difficulty'],
                explanation=q_data['explanation'],
                order_index=i
            )
            db.session.add(question)

        db.session.commit()
        db.session.refresh(quiz)

        yield quiz

        # Cleanup: delete quiz (cascade deletes questions)
        db.session.delete(quiz)
        db.session.commit()


@pytest.fixture(scope='function')
def auth_headers(client, sample_user):
    """
    Create authentication headers for API testing.

    Logs in the sample_user and returns headers with session cookie.
    """
    # Login user
    with client.session_transaction() as sess:
        sess['user_id'] = sample_user.id
        sess['username'] = sample_user.username

    return {'Content-Type': 'application/json'}


@pytest.fixture(scope='function')
def completed_attempt(app, sample_user, sample_quiz):
    """
    Create a completed quiz attempt for testing.

    Returns an Attempt object with all questions answered.
    """
    with app.app_context():
        # Create attempt
        attempt = Attempt(
            user_id=sample_user.id,
            quiz_id=sample_quiz.id
        )
        db.session.add(attempt)
        db.session.flush()

        # Get questions
        questions = Question.query.filter_by(quiz_id=sample_quiz.id).all()

        # Answer all questions (3 correct, 2 incorrect)
        correct_count = 0
        for i, question in enumerate(questions):
            is_correct = i < 3  # First 3 are correct
            selected = question.correct_answer if is_correct else (question.correct_answer + 1) % 4

            answer = UserAnswer(
                attempt_id=attempt.id,
                question_id=question.id,
                selected_answer=selected,
                is_correct=is_correct
            )
            db.session.add(answer)

            if is_correct:
                correct_count += 1

        # Complete the attempt
        attempt.complete(score=correct_count)

        db.session.commit()
        db.session.refresh(attempt)

        yield attempt

        # Cleanup handled by cascade delete from sample_user


@pytest.fixture(scope='function')
def in_progress_attempt(app, sample_user, sample_quiz):
    """
    Create an in-progress quiz attempt for testing.

    Returns an Attempt object that is not yet completed.
    """
    with app.app_context():
        attempt = Attempt(
            user_id=sample_user.id,
            quiz_id=sample_quiz.id
        )
        db.session.add(attempt)
        db.session.commit()
        db.session.refresh(attempt)

        yield attempt

        # Cleanup handled by cascade delete from sample_user


@pytest.fixture(autouse=True)
def reset_db_session(app):
    """
    Automatically reset database session after each test.

    This fixture runs automatically for every test.
    """
    yield

    with app.app_context():
        db.session.remove()
