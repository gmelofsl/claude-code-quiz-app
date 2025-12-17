from flask import Flask, render_template, request, session, redirect, url_for
import random
import os
from functools import wraps
from quiz_data import (QUIZ_DATA, get_all_topics, get_total_questions,
                       get_all_difficulties, get_questions_by_difficulty,
                       get_questions_by_topic_and_difficulty, get_difficulty_stats)
from models import db, User, Quiz, Question, Attempt, UserAnswer
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'claude-quiz-app-secret-key-2025'

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quiz_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Landing page"""
    # If user is logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/start', methods=['POST'])
@login_required
def start_quiz():
    """Initialize quiz session with database integration"""
    user_id = session.get('user_id')
    quiz_id = request.form.get('quiz_id')

    if not quiz_id:
        return redirect(url_for('dashboard'))

    # Get quiz and questions from database
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return redirect(url_for('dashboard'))

    questions_db = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.order_index).all()

    if not questions_db:
        return redirect(url_for('dashboard'))

    # Convert questions to dictionary format for session storage
    questions = [q.to_dict() for q in questions_db]

    # Shuffle questions
    random.shuffle(questions)

    # Create new attempt record
    new_attempt = Attempt(
        user_id=user_id,
        quiz_id=quiz_id,
        started_at=datetime.utcnow()
    )
    db.session.add(new_attempt)
    db.session.commit()

    # Initialize session
    session['quiz_id'] = quiz_id
    session['attempt_id'] = new_attempt.id
    session['questions'] = questions
    session['current_index'] = 0
    session['score'] = 0
    session['answers'] = []

    return redirect(url_for('question'))

@app.route('/question')
@login_required
def question():
    """Display current question"""
    if 'questions' not in session:
        return redirect(url_for('dashboard'))

    current_index = session['current_index']
    questions = session['questions']

    if current_index >= len(questions):
        return redirect(url_for('results'))

    current_question = questions[current_index]
    progress = ((current_index) / len(questions)) * 100

    return render_template('question.html',
                         question=current_question,
                         question_num=current_index + 1,
                         total_questions=len(questions),
                         progress=progress)

@app.route('/submit', methods=['POST'])
@login_required
def submit_answer():
    """Process submitted answer"""
    if 'questions' not in session:
        return redirect(url_for('dashboard'))

    current_index = session['current_index']
    questions = session['questions']
    current_question = questions[current_index]

    selected_answer = int(request.form.get('answer', -1))
    correct_answer = current_question['correct']

    is_correct = selected_answer == correct_answer
    if is_correct:
        session['score'] = session.get('score', 0) + 1

    # Store answer history (with question id and category)
    answers = session.get('answers', [])
    answers.append({
        'id': current_question.get('id'),  # Question ID from database
        'question': current_question['question'],
        'category': current_question.get('category', current_question.get('topic', 'General')),
        'difficulty': current_question.get('difficulty', 'unknown'),
        'selected': selected_answer,
        'correct': correct_answer,
        'is_correct': is_correct,
        'explanation': current_question['explanation'],
        'options': current_question['options']
    })
    session['answers'] = answers

    # Move to next question
    session['current_index'] = current_index + 1

    return redirect(url_for('question'))

@app.route('/results')
@login_required
def results():
    """Display final results and save to database"""
    if 'questions' not in session:
        return redirect(url_for('dashboard'))

    score = session.get('score', 0)
    total = len(session['questions'])
    percentage = (score / total * 100) if total > 0 else 0
    answers = session.get('answers', [])
    attempt_id = session.get('attempt_id')
    quiz_id = session.get('quiz_id')

    # Save results to database
    if attempt_id:
        attempt = Attempt.query.get(attempt_id)
        if attempt:
            # Update attempt record
            attempt.completed_at = datetime.utcnow()
            attempt.score = score
            attempt.total_questions = total
            attempt.percentage = percentage

            # Create UserAnswer records for each answer
            for answer in answers:
                question_id = answer.get('id')  # Question ID from to_dict()
                if question_id:
                    user_answer = UserAnswer(
                        attempt_id=attempt_id,
                        question_id=question_id,
                        selected_answer=answer['selected'],
                        is_correct=answer['is_correct'],
                        answered_at=datetime.utcnow()
                    )
                    db.session.add(user_answer)

            db.session.commit()

    # Determine performance level
    if percentage >= 90:
        performance = "Excellent! 🌟"
        message = "You have mastered AI development concepts!"
    elif percentage >= 70:
        performance = "Great Job! 🎯"
        message = "You have a solid understanding of the concepts."
    elif percentage >= 50:
        performance = "Good Effort! 📚"
        message = "You're on the right track. Review the topics you missed."
    else:
        performance = "Keep Learning! 💪"
        message = "Consider reviewing the concepts again."

    # Get category breakdown (using 'category' or 'topic' for backwards compatibility)
    category_stats = {}
    for answer in answers:
        category = answer.get('category', answer.get('topic', 'General'))
        if category not in category_stats:
            category_stats[category] = {'correct': 0, 'total': 0}
        category_stats[category]['total'] += 1
        if answer['is_correct']:
            category_stats[category]['correct'] += 1

    # Get quiz information for display
    quiz = Quiz.query.get(quiz_id) if quiz_id else None

    return render_template('results.html',
                         score=score,
                         total=total,
                         percentage=round(percentage, 1),
                         performance=performance,
                         message=message,
                         answers=answers,
                         category_stats=category_stats,
                         quiz=quiz,
                         attempt_id=attempt_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login or create new user"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()

        if not username:
            return render_template('login.html', error='Username is required')

        # Check if user exists
        user = User.query.filter_by(username=username).first()

        if user:
            # User exists, log them in
            session['user_id'] = user.id
            session['username'] = user.username
            user.last_active = datetime.utcnow()
            db.session.commit()
        else:
            # Create new user
            new_user = User(username=username)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            session['username'] = new_user.username

        return redirect(url_for('dashboard'))

    # GET request - show login form
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard with quiz selection and user statistics"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if not user:
        return redirect(url_for('login'))

    # Get user statistics
    stats = user.get_stats()

    # Get all quizzes
    quizzes = Quiz.query.all()

    # Get recent attempts (last 5)
    recent_attempts = Attempt.query.filter_by(user_id=user_id)\
        .filter(Attempt.completed_at.isnot(None))\
        .order_by(Attempt.completed_at.desc())\
        .limit(5)\
        .all()

    # Get category-specific stats
    category_stats = {}
    for quiz in quizzes:
        quiz_attempts = Attempt.query.filter_by(user_id=user_id, quiz_id=quiz.id)\
            .filter(Attempt.completed_at.isnot(None))\
            .all()

        if quiz_attempts:
            best_score = max(a.percentage for a in quiz_attempts)
            attempt_count = len(quiz_attempts)
        else:
            best_score = 0
            attempt_count = 0

        category_stats[quiz.id] = {
            'best_score': round(best_score, 1),
            'attempt_count': attempt_count
        }

    return render_template('dashboard.html',
                         user=user,
                         stats=stats,
                         quizzes=quizzes,
                         recent_attempts=recent_attempts,
                         category_stats=category_stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
