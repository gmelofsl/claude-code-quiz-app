"""
SQLite to PostgreSQL migration script.

This script migrates data from the old SQLite database (quiz_app.db) to the new
production database schema. It handles:
- Users (with enhanced fields)
- Quizzes
- Questions
- Attempts
- UserAnswers

Usage:
    # Dry run (preview changes without committing)
    python scripts/migrate_sqlite_to_pg.py --dry-run

    # Execute migration
    python scripts/migrate_sqlite_to_pg.py

    # Migrate to production database
    FLASK_ENV=production python scripts/migrate_sqlite_to_pg.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models import User, Quiz, Question, Attempt, UserAnswer

# SQLAlchemy for reading old database
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


class DataMigrator:
    """Handles migration from old SQLite schema to new production schema."""

    def __init__(self, old_db_path, dry_run=False):
        """
        Initialize migrator.

        Args:
            old_db_path: Path to old SQLite database
            dry_run: If True, preview changes without committing
        """
        self.old_db_path = old_db_path
        self.dry_run = dry_run
        self.stats = {
            'users': 0,
            'quizzes': 0,
            'questions': 0,
            'attempts': 0,
            'user_answers': 0
        }

        # Connect to old database
        old_db_uri = f'sqlite:///{old_db_path}'
        self.old_engine = create_engine(old_db_uri)
        self.old_metadata = MetaData()
        self.old_metadata.reflect(bind=self.old_engine)
        OldSession = sessionmaker(bind=self.old_engine)
        self.old_session = OldSession()

    def migrate(self):
        """Execute migration."""
        print("=" * 70)
        print("🔄 DATABASE MIGRATION: SQLite → Production Schema")
        print("=" * 70)
        print(f"Source: {self.old_db_path}")
        print(f"Mode: {'DRY RUN (no changes will be saved)' if self.dry_run else 'LIVE MIGRATION'}")
        print("=" * 70)

        try:
            # Step 1: Migrate Users
            user_mapping = self.migrate_users()

            # Step 2: Migrate Quizzes
            quiz_mapping = self.migrate_quizzes()

            # Step 3: Migrate Questions
            question_mapping = self.migrate_questions(quiz_mapping)

            # Step 4: Migrate Attempts
            attempt_mapping = self.migrate_attempts(user_mapping, quiz_mapping)

            # Step 5: Migrate UserAnswers
            self.migrate_user_answers(attempt_mapping, question_mapping)

            # Commit or rollback
            if self.dry_run:
                db.session.rollback()
                print("\n" + "=" * 70)
                print("🔍 DRY RUN COMPLETED - No changes were saved")
            else:
                db.session.commit()
                print("\n" + "=" * 70)
                print("✅ MIGRATION COMPLETED SUCCESSFULLY!")

            # Print statistics
            print("=" * 70)
            print("📊 MIGRATION STATISTICS:")
            print("-" * 70)
            for entity, count in self.stats.items():
                print(f"   {entity.capitalize()}: {count}")
            print("=" * 70)

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR: Migration failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def migrate_users(self):
        """Migrate users from old to new schema."""
        print("\n👤 Migrating users...")

        old_users_table = Table('users', self.old_metadata, autoload_with=self.old_engine)
        old_users = self.old_session.execute(old_users_table.select()).fetchall()

        user_mapping = {}  # old_id -> new_user

        for old_user in old_users:
            # Create new user with enhanced fields
            new_user = User(
                username=old_user.username,
                email=f"{old_user.username}@temp.quiz-app.local",  # Placeholder email
                password_hash=None,  # Will require password creation on first login
                is_active=True,
                is_admin=False,
                email_verified=False,  # Needs verification
                created_at=old_user.created_at,
                last_active=old_user.last_active
            )

            db.session.add(new_user)
            db.session.flush()  # Get new user ID

            user_mapping[old_user.id] = new_user
            self.stats['users'] += 1

        print(f"   ✓ Migrated {self.stats['users']} users")
        print(f"   ⚠️  Note: Users will need to set passwords and verify emails on first login")

        return user_mapping

    def migrate_quizzes(self):
        """Migrate quizzes."""
        print("\n📚 Migrating quizzes...")

        old_quizzes_table = Table('quizzes', self.old_metadata, autoload_with=self.old_engine)
        old_quizzes = self.old_session.execute(old_quizzes_table.select()).fetchall()

        quiz_mapping = {}  # old_id -> new_quiz

        for old_quiz in old_quizzes:
            new_quiz = Quiz(
                category=old_quiz.category,
                title=old_quiz.title,
                description=old_quiz.description,
                icon=getattr(old_quiz, 'icon', '📝'),
                created_at=old_quiz.created_at
            )

            db.session.add(new_quiz)
            db.session.flush()

            quiz_mapping[old_quiz.id] = new_quiz
            self.stats['quizzes'] += 1

        print(f"   ✓ Migrated {self.stats['quizzes']} quizzes")

        return quiz_mapping

    def migrate_questions(self, quiz_mapping):
        """Migrate questions."""
        print("\n❓ Migrating questions...")

        old_questions_table = Table('questions', self.old_metadata, autoload_with=self.old_engine)
        old_questions = self.old_session.execute(old_questions_table.select()).fetchall()

        question_mapping = {}  # old_id -> new_question

        for old_question in old_questions:
            if old_question.quiz_id not in quiz_mapping:
                print(f"   ⚠️  Skipping question {old_question.id}: quiz {old_question.quiz_id} not found")
                continue

            new_question = Question(
                quiz_id=quiz_mapping[old_question.quiz_id].id,
                question_text=old_question.question_text,
                option_1=old_question.option_1,
                option_2=old_question.option_2,
                option_3=old_question.option_3,
                option_4=old_question.option_4,
                correct_answer=old_question.correct_answer,
                explanation=old_question.explanation,
                difficulty=old_question.difficulty,
                order_index=old_question.order_index
            )

            db.session.add(new_question)
            db.session.flush()

            question_mapping[old_question.id] = new_question
            self.stats['questions'] += 1

        print(f"   ✓ Migrated {self.stats['questions']} questions")

        return question_mapping

    def migrate_attempts(self, user_mapping, quiz_mapping):
        """Migrate attempts."""
        print("\n📝 Migrating attempts...")

        old_attempts_table = Table('attempts', self.old_metadata, autoload_with=self.old_engine)
        old_attempts = self.old_session.execute(old_attempts_table.select()).fetchall()

        attempt_mapping = {}  # old_id -> new_attempt

        for old_attempt in old_attempts:
            if old_attempt.user_id not in user_mapping:
                print(f"   ⚠️  Skipping attempt {old_attempt.id}: user {old_attempt.user_id} not found")
                continue
            if old_attempt.quiz_id not in quiz_mapping:
                print(f"   ⚠️  Skipping attempt {old_attempt.id}: quiz {old_attempt.quiz_id} not found")
                continue

            new_attempt = Attempt(
                user_id=user_mapping[old_attempt.user_id].id,
                quiz_id=quiz_mapping[old_attempt.quiz_id].id,
                started_at=old_attempt.started_at,
                completed_at=old_attempt.completed_at,
                score=old_attempt.score,
                total_questions=old_attempt.total_questions,
                percentage=old_attempt.percentage
            )

            # Calculate time_taken if both timestamps exist
            if new_attempt.started_at and new_attempt.completed_at:
                time_delta = new_attempt.completed_at - new_attempt.started_at
                new_attempt.time_taken = int(time_delta.total_seconds())

            db.session.add(new_attempt)
            db.session.flush()

            attempt_mapping[old_attempt.id] = new_attempt
            self.stats['attempts'] += 1

        print(f"   ✓ Migrated {self.stats['attempts']} attempts")

        return attempt_mapping

    def migrate_user_answers(self, attempt_mapping, question_mapping):
        """Migrate user answers."""
        print("\n✍️  Migrating user answers...")

        old_user_answers_table = Table('user_answers', self.old_metadata, autoload_with=self.old_engine)
        old_user_answers = self.old_session.execute(old_user_answers_table.select()).fetchall()

        for old_answer in old_user_answers:
            if old_answer.attempt_id not in attempt_mapping:
                continue
            if old_answer.question_id not in question_mapping:
                continue

            new_answer = UserAnswer(
                attempt_id=attempt_mapping[old_answer.attempt_id].id,
                question_id=question_mapping[old_answer.question_id].id,
                selected_answer=old_answer.selected_answer,
                is_correct=old_answer.is_correct,
                answered_at=old_answer.answered_at
            )

            db.session.add(new_answer)
            self.stats['user_answers'] += 1

        print(f"   ✓ Migrated {self.stats['user_answers']} user answers")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Migrate SQLite database to production schema')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without committing')
    parser.add_argument('--old-db', default='../quiz_app.db', help='Path to old SQLite database')
    args = parser.parse_args()

    # Resolve old database path
    old_db_path = Path(__file__).parent.parent / args.old_db
    old_db_path = old_db_path.resolve()

    if not old_db_path.exists():
        print(f"❌ ERROR: Old database not found at {old_db_path}")
        sys.exit(1)

    # Create app and run migration
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)

    with app.app_context():
        migrator = DataMigrator(old_db_path, dry_run=args.dry_run)
        migrator.migrate()


if __name__ == '__main__':
    main()
