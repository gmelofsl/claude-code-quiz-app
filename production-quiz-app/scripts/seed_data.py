"""
Database seeding script for quiz content.

This script populates the production database with quiz categories and questions
from the quiz_data.py file.

Usage:
    python scripts/seed_data.py [--clear]

Options:
    --clear     Clear existing quiz data before seeding (WARNING: destructive)
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models import Question, Quiz  # noqa: E402

# Import quiz data from original location
original_quiz_data_path = Path(__file__).parent.parent.parent / "quiz_data.py"
if original_quiz_data_path.exists():
    sys.path.insert(0, str(original_quiz_data_path.parent))
    from quiz_data import QUIZ_DATA
else:
    print(f"ERROR: quiz_data.py not found at {original_quiz_data_path}")
    sys.exit(1)


# Quiz metadata by category
QUIZ_CATEGORIES = {
    "Agent Fundamentals": {
        "title": "Agent Fundamentals",
        "description": "Test your knowledge of AI agent architecture, patterns, and design principles.",
        "icon": "🤖",
    },
    "Prompt Engineering": {
        "title": "Prompt Engineering",
        "description": "Master the art of crafting effective prompts for large language models.",
        "icon": "✍️",
    },
    "Model Selection & Context Management": {
        "title": "Model Selection & Context Management",
        "description": "Learn about choosing the right models and managing context windows effectively.",
        "icon": "🎯",
    },
}


def clear_quiz_data():
    """Clear all quiz-related data from the database."""
    print("WARNING: Clearing existing quiz data...")

    # Delete in order (respecting foreign keys)
    deleted_answers = db.session.query(Question).delete()
    deleted_questions = db.session.query(Quiz).delete()

    db.session.commit()

    print(f"   Deleted {deleted_questions} questions")
    print(f"   Deleted {deleted_answers} quizzes")


def seed_quizzes():
    """Create quiz categories."""
    print("\n[QUIZZES] Creating quiz categories...")

    quizzes = {}
    for category, metadata in QUIZ_CATEGORIES.items():
        quiz = Quiz(
            category=category,
            title=metadata["title"],
            description=metadata["description"],
            icon=metadata.get("icon", "*"),
        )
        db.session.add(quiz)
        quizzes[category] = quiz
        print(f"   [OK] Created quiz: {category}")

    db.session.flush()  # Flush to get quiz IDs
    return quizzes


def seed_questions(quizzes):
    """Create questions for each quiz."""
    print("\n[QUESTIONS] Creating questions...")

    # Group questions by category
    questions_by_category = {}
    for question_data in QUIZ_DATA:
        category = question_data["category"]
        if category not in questions_by_category:
            questions_by_category[category] = []
        questions_by_category[category].append(question_data)

    total_questions = 0
    for category, questions_list in questions_by_category.items():
        if category not in quizzes:
            print(f"   [WARNING] Category '{category}' not found in QUIZ_CATEGORIES")
            continue

        quiz = quizzes[category]

        for idx, question_data in enumerate(questions_list):
            question = Question(
                quiz_id=quiz.id,
                question_text=question_data["question"],
                option_1=question_data["options"][0],
                option_2=question_data["options"][1],
                option_3=question_data["options"][2],
                option_4=question_data["options"][3],
                correct_answer=question_data["correct"],
                explanation=question_data["explanation"],
                difficulty=question_data["difficulty"],
                order_index=idx,
            )
            db.session.add(question)
            total_questions += 1

        print(f"   [OK] Created {len(questions_list)} questions for '{category}'")

    return total_questions


def seed_database(clear_existing=False):
    """Main seeding function."""
    print("=" * 60)
    print("DATABASE SEEDING SCRIPT")
    print("=" * 60)

    app = create_app("development")

    with app.app_context():
        # Clear existing data if requested
        if clear_existing:
            if (
                input("\nWARNING: Are you sure you want to clear all quiz data? (yes/no): ").lower()
                != "yes"
            ):
                print("Aborted.")
                return
            clear_quiz_data()

        # Check if quizzes already exist
        existing_quiz_count = Quiz.query.count()
        if existing_quiz_count > 0 and not clear_existing:
            print(f"\nWARNING: {existing_quiz_count} quiz(zes) already exist in the database.")
            response = input("Continue anyway? This may create duplicates. (yes/no): ")
            if response.lower() != "yes":
                print("Aborted.")
                return

        # Seed quizzes
        quizzes = seed_quizzes()

        # Seed questions
        total_questions = seed_questions(quizzes)

        # Commit all changes
        try:
            db.session.commit()
            print("\n" + "=" * 60)
            print("[SUCCESS] DATABASE SEEDING COMPLETED!")
            print("=" * 60)
            print(f"   Quizzes created: {len(quizzes)}")
            print(f"   Questions created: {total_questions}")
            print("=" * 60)
        except Exception as e:
            db.session.rollback()
            print(f"\n[ERROR] Failed to commit changes: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    clear_existing = "--clear" in sys.argv

    try:
        seed_database(clear_existing=clear_existing)
    except KeyboardInterrupt:
        print("\n\nAborted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
