# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Development Quiz App - A Flask-based educational platform for testing knowledge of AI software development concepts including Agent Fundamentals, Prompt Engineering, and Model Selection & Context Management.

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize/reset database (drops existing tables and reseeds)
python init_db.py

# Run the Flask development server
python app.py
```

Access at: http://localhost:5000

## Database Architecture

**State Management Strategy**: Hybrid approach
- **During Quiz**: Session-based (fast, no DB writes per question)
- **After Completion**: Database persistence (Attempt and UserAnswer records created)

**Schema Overview**:
```
users ────┐
          ├──> attempts ───> user_answers
quizzes ──┘         └──────> questions
```

### Key Relationships

1. **User → Attempts**: One user has many quiz attempts (cascade delete)
2. **Quiz → Questions**: One quiz contains many questions (cascade delete)
3. **Attempt → UserAnswers**: One attempt contains many individual question answers (cascade delete)
4. **Question ↔ UserAnswer**: Questions track which user answers reference them

### Critical Model Methods

- `Question.to_dict()`: Converts DB model to session-compatible dictionary format for quiz flow
- `User.get_stats()`: Calculates total attempts, average score, best score (filters only completed attempts)
- `Attempt.get_formatted_date()`: Returns formatted completion date or "In Progress"

## Application Flow

```
Landing (/)
  → Login (/login) [username-only, creates user if doesn't exist]
    → Dashboard (/dashboard) [displays stats, quiz cards, recent activity]
      → Start Quiz (POST /start with quiz_id)
        → Question Loop (/question → POST /submit)
          → Results (/results) [saves Attempt + UserAnswers to DB]
            → Dashboard or Retake
```

### Session Variables (Quiz Flow)

During active quiz:
- `quiz_id`: ID of quiz being taken
- `attempt_id`: ID of Attempt record (created at start)
- `questions`: List of question dictionaries (from `Question.to_dict()`)
- `current_index`: Current question index
- `score`: Running score count
- `answers`: List of answer dictionaries (saved to DB on completion)

For authentication:
- `user_id`: Current logged-in user ID
- `username`: Current logged-in username

## Adding Quiz Content

Questions are defined in `quiz_data.py` as `QUIZ_DATA` list. Format:

```python
{
    "category": "Agent Fundamentals",  # Must match quiz category
    "question": "Question text here?",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct": 0,  # Index of correct option (0-3)
    "difficulty": "easy",  # easy, medium, or hard
    "explanation": "Explanation of the correct answer"
}
```

After modifying `QUIZ_DATA`, run `python init_db.py` to reseed the database.

## Database Initialization

`init_db.py` performs:
1. **Drop all tables** (⚠️ destructive - all user data lost)
2. **Create tables** from models.py
3. **Seed quizzes** by grouping `QUIZ_DATA` by category
4. **Seed questions** with order_index for each quiz

Default categories:
- Agent Fundamentals (🤖)
- Prompt Engineering (✍️)
- Model Selection & Context Management (🎯)

## Authentication System

**Username-only authentication** - No passwords required
- Login creates new user automatically if username doesn't exist
- `@login_required` decorator protects routes (redirects to /login)
- Session stores `user_id` and `username`
- User.last_active updated on each login

## Key Routes

### Public Routes
- `GET /` - Landing page (redirects to dashboard if logged in)
- `GET /login` - Login form
- `POST /login` - Process login/create user
- `GET /logout` - Clear session

### Protected Routes (require login)
- `GET /dashboard` - User dashboard with stats and quiz selection
- `POST /start` - Initialize quiz (creates Attempt record, loads questions, shuffles)
- `GET /question` - Display current question
- `POST /submit` - Process answer (stores in session temporarily)
- `GET /results` - Final results (commits Attempt and UserAnswer records to DB)

## Template Structure

**Base Template** (`base.html`):
- Purple gradient design theme
- Conditional navbar (shown only when logged in)
- Contains username display and logout link

**Page Templates**:
- `index.html` - Landing page with category overview
- `login.html` - Username entry form
- `dashboard.html` - Quiz selection cards, stats grid, recent activity
- `question.html` - Question display with progress bar and keyboard shortcuts (1-4)
- `results.html` - Score, category breakdown, answer review with explanations

## Dashboard Statistics

**User Stats** (calculated in `User.get_stats()`):
- Total attempts (only completed)
- Average score percentage
- Best score percentage

**Per-Quiz Stats** (calculated in dashboard route):
- Best score for each quiz category
- Number of attempts per category

## Common Development Tasks

### Add a New Quiz Category

1. Add questions to `QUIZ_DATA` in quiz_data.py with new `category` value
2. Update `quiz_categories` dict in `init_db.py` with description and icon
3. Run `python init_db.py` to reseed
4. New quiz card appears automatically on dashboard

### Add New Route

Example pattern:
```python
@app.route('/new-route')
@login_required  # If authentication required
def new_route():
    user_id = session.get('user_id')
    # Query database
    # Process data
    return render_template('template.html', data=data)
```

### Query Patterns

Common queries used throughout:
```python
# Get user with stats
user = User.query.get(user_id)
stats = user.get_stats()

# Get completed attempts with quiz info
attempts = Attempt.query.filter_by(user_id=user_id)\
    .filter(Attempt.completed_at.isnot(None))\
    .order_by(Attempt.completed_at.desc())\
    .all()

# Get questions for a quiz
questions = Question.query.filter_by(quiz_id=quiz_id)\
    .order_by(Question.order_index)\
    .all()
```

## Custom Agents & Slash Commands

This project includes specialized agents accessible via slash commands:

### Available Agents

**Backend Agent** (`/backend-agent`)
- Specialized for Flask backend development
- Handles routes, database models, business logic
- Implements features like leaderboards, timed quizzes, analytics
- Example: `/backend-agent Add timed quiz mode with countdown`

**Quiz Content Agent** (`/quiz-content-agent`)
- AI-powered question creation and validation
- Generates new quiz questions on any AI/ML topic
- Reviews question quality and explanations
- Analyzes question distribution and identifies gaps
- Detects duplicate questions
- Example: `/quiz-content-agent Generate 5 medium questions about RAG systems`
- See `QUIZ_CONTENT_AGENT_GUIDE.md` for detailed usage

### Creating Custom Agents

To create your own agent:
1. Create a new `.md` file in `.claude/commands/`
2. Add front matter with `description` and `argument-hint`
3. Write the agent's instructions and capabilities
4. Use via `/your-command-name [args]`

## Known Limitations / Future Enhancements

**Not Yet Implemented**:
- ~~`/history` route to view all past attempts~~ ✅ COMPLETED
- ~~`/history/<attempt_id>` route for detailed review of specific past attempt~~ ✅ COMPLETED
- Leaderboard system (cross-user rankings)
- Timed quizzes with countdown
- Adaptive difficulty based on performance
- Question bookmarking
- Study mode vs exam mode

**Database**:
- SQLite (suitable for training/demo, migrate to PostgreSQL for production)
- No migration system (uses drop/recreate via init_db.py)
- User data lost on database reset

## Debugging Tips

**Database Issues**:
- Check `quiz_app.db` exists in project root
- Run `python init_db.py` to reset/recreate database
- Verify questions loaded: Check output of init_db.py for question count per quiz

**Session Issues**:
- Flask sessions stored client-side (cookie-based)
- Secret key in app.py (change for production)
- Session cleared on logout or can expire

**Quiz Not Starting**:
- Verify `quiz_id` POSTed to /start route
- Check questions exist for that quiz_id in database
- Ensure user is logged in (session has `user_id`)
