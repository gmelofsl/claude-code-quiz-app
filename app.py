from flask import Flask, render_template, request, session, redirect, url_for
import random
from quiz_data import QUIZ_DATA, get_all_topics, get_total_questions

app = Flask(__name__)
app.secret_key = 'claude-quiz-app-secret-key-2025'

@app.route('/')
def index():
    """Landing page with quiz intro"""
    session.clear()
    return render_template('index.html',
                         total_questions=get_total_questions(),
                         topics=get_all_topics())

@app.route('/start', methods=['POST'])
def start_quiz():
    """Initialize quiz session"""
    quiz_mode = request.form.get('mode', 'all')

    if quiz_mode == 'all':
        questions = QUIZ_DATA.copy()
    else:
        questions = [q for q in QUIZ_DATA if q['topic'] == quiz_mode]

    # Shuffle questions
    random.shuffle(questions)

    # Initialize session
    session['questions'] = questions
    session['current_index'] = 0
    session['score'] = 0
    session['answers'] = []
    session['mode'] = quiz_mode

    return redirect(url_for('question'))

@app.route('/question')
def question():
    """Display current question"""
    if 'questions' not in session:
        return redirect(url_for('index'))

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
def submit_answer():
    """Process submitted answer"""
    if 'questions' not in session:
        return redirect(url_for('index'))

    current_index = session['current_index']
    questions = session['questions']
    current_question = questions[current_index]

    selected_answer = int(request.form.get('answer', -1))
    correct_answer = current_question['correct']

    is_correct = selected_answer == correct_answer
    if is_correct:
        session['score'] = session.get('score', 0) + 1

    # Store answer history
    answers = session.get('answers', [])
    answers.append({
        'question': current_question['question'],
        'topic': current_question['topic'],
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
def results():
    """Display final results"""
    if 'questions' not in session:
        return redirect(url_for('index'))

    score = session.get('score', 0)
    total = len(session['questions'])
    percentage = (score / total * 100) if total > 0 else 0
    answers = session.get('answers', [])

    # Determine performance level
    if percentage >= 90:
        performance = "Excellent! 🌟"
        message = "You have mastered Claude Code concepts!"
    elif percentage >= 70:
        performance = "Great Job! 🎯"
        message = "You have a solid understanding of the concepts."
    elif percentage >= 50:
        performance = "Good Effort! 📚"
        message = "You're on the right track. Review the topics you missed."
    else:
        performance = "Keep Learning! 💪"
        message = "Consider reviewing the Claude Code documentation again."

    # Get topic breakdown
    topic_stats = {}
    for answer in answers:
        topic = answer['topic']
        if topic not in topic_stats:
            topic_stats[topic] = {'correct': 0, 'total': 0}
        topic_stats[topic]['total'] += 1
        if answer['is_correct']:
            topic_stats[topic]['correct'] += 1

    return render_template('results.html',
                         score=score,
                         total=total,
                         percentage=round(percentage, 1),
                         performance=performance,
                         message=message,
                         answers=answers,
                         topic_stats=topic_stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
