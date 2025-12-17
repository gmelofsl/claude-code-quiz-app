"""
Database initialization and seeding script for the AI Development Quiz App
"""

from app import app, db
from models import User, Quiz, Question, Attempt, UserAnswer
from quiz_data import QUIZ_DATA

def create_database():
    """Create all database tables"""
    with app.app_context():
        # Drop all existing tables (for fresh start)
        db.drop_all()
        print("Dropped existing tables")

        # Create all tables
        db.create_all()
        print("Created database tables successfully")


def seed_quizzes_and_questions():
    """Seed quizzes and questions from quiz_data.py"""
    with app.app_context():
        # Define the quiz categories for AI Development
        quiz_categories = {
            'Agent Fundamentals': {
                'description': 'Understanding AI agents, their architecture, and when to use them',
                'icon': '🤖'
            },
            'Prompt Engineering': {
                'description': 'Crafting effective prompts and managing AI interactions',
                'icon': '✍️'
            },
            'Model Selection & Context Management': {
                'description': 'Choosing the right model and managing context windows',
                'icon': '🎯'
            }
        }

        # Group questions by category (or topic for old format)
        questions_by_category = {}
        for q in QUIZ_DATA:
            # Support both 'category' (new format) and 'topic' (old format)
            category = q.get('category') or q.get('topic', 'General')
            if category not in questions_by_category:
                questions_by_category[category] = []
            questions_by_category[category].append(q)

        # Create quizzes and questions
        for category_name, questions_list in questions_by_category.items():
            # Get category info or use defaults
            category_info = quiz_categories.get(category_name, {
                'description': f'Quiz on {category_name}',
                'icon': '📝'
            })

            # Create quiz
            quiz = Quiz(
                category=category_name,
                title=category_name,
                description=category_info['description']
            )
            db.session.add(quiz)
            db.session.flush()  # Get the quiz ID

            # Create questions for this quiz
            for index, q_data in enumerate(questions_list):
                question = Question(
                    quiz_id=quiz.id,
                    question_text=q_data['question'],
                    option_1=q_data['options'][0],
                    option_2=q_data['options'][1],
                    option_3=q_data['options'][2],
                    option_4=q_data['options'][3],
                    correct_answer=q_data['correct'],
                    explanation=q_data['explanation'],
                    difficulty=q_data.get('difficulty', 'medium'),
                    order_index=index
                )
                db.session.add(question)

            print(f"Created quiz '{category_name}' with {len(questions_list)} questions")

        # Commit all changes
        db.session.commit()
        print(f"\nSuccessfully seeded {len(questions_by_category)} quizzes")


def create_sample_user():
    """Create a sample user for testing (optional)"""
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username='demo').first()
        if existing_user:
            print("Sample user 'demo' already exists")
            return

        # Create sample user
        demo_user = User(username='demo')
        db.session.add(demo_user)
        db.session.commit()
        print("Created sample user 'demo'")


def verify_database():
    """Verify database contents"""
    with app.app_context():
        quiz_count = Quiz.query.count()
        question_count = Question.query.count()
        user_count = User.query.count()

        print("\n=== Database Verification ===")
        print(f"Quizzes: {quiz_count}")
        print(f"Questions: {question_count}")
        print(f"Users: {user_count}")

        # Show quiz details
        print("\n=== Quiz Details ===")
        quizzes = Quiz.query.all()
        for quiz in quizzes:
            print(f"- {quiz.title}: {quiz.get_question_count()} questions")


def main():
    """Main initialization function"""
    print("=== Initializing Quiz App Database ===\n")

    # Step 1: Create database tables
    create_database()

    # Step 2: Seed quizzes and questions
    seed_quizzes_and_questions()

    # Step 3: Create sample user (optional)
    # create_sample_user()

    # Step 4: Verify database
    verify_database()

    print("\n=== Database initialization complete! ===")


if __name__ == '__main__':
    main()
