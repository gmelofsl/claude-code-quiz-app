# Development Guide

Guide for developers working on the Production Quiz App.

## Quick Start

```bash
git clone https://github.com/your-username/production-quiz-app.git
cd production-quiz-app
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env
flask db upgrade
python scripts/seed_data.py
flask run
```

Visit: http://localhost:5000

## Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture overview.

## Development Workflow

1. **Create branch**: `git checkout -b feature/my-feature develop`
2. **Make changes**: Follow coding standards below
3. **Run tests**: `pytest tests/ --cov=app`
4. **Format code**: `black app/ tests/ && isort app/ tests/`
5. **Commit**: `git commit -m "feat: add feature"`
6. **Push and PR**: `git push origin feature/my-feature`

## Coding Standards

- **Style**: PEP 8, Black (line-length: 100), isort
- **Linting**: Flake8 (max-complexity: 10)
- **Naming**: Classes=PascalCase, functions=snake_case, constants=UPPER_SNAKE_CASE
- **Docstrings**: Google-style
- **Type hints**: Use typing module

### Example Code

```python
from typing import Optional, Tuple

def authenticate_user(username: str, password: str) -> Tuple[Optional[User], Optional[str]]:
    """
    Authenticate user by username and password.

    Args:
        username: Username or email address
        password: Plain text password

    Returns:
        Tuple of (user, error_message)
    """
    pass
```

## Testing

### Run Tests

```bash
pytest                              # All tests
pytest tests/unit/                  # Unit tests only
pytest tests/integration/           # Integration tests only
pytest --cov=app --cov-report=html  # With coverage
pytest -x                           # Stop on first failure
pytest -v                           # Verbose
```

### Writing Tests

```python
# tests/unit/test_models.py
def test_set_password(app):
    with app.app_context():
        user = UserFactory()
        user.set_password("TestPass123")
        assert user.check_password("TestPass123")

# tests/integration/test_auth_flow.py
def test_login(client):
    response = client.post('/auth/login', data={
        'username_or_email': 'test',
        'password': 'TestPass123'
    })
    assert response.status_code == 200
```

### Test Fixtures

Available in `tests/conftest.py`:
- `app`: Flask application
- `client`: Test client
- `sample_user`: User with password "TestPass123"
- `sample_quiz`: Quiz with 5 questions
- `auth_headers`: Authenticated session headers

### Test Factories

Available in `tests/factories.py`:
- `UserFactory()`: Create user
- `QuizFactory()`: Create quiz
- `QuestionFactory(quiz=quiz)`: Create question
- `AttemptFactory.create_completed()`: Create completed attempt

## Database Development

### Migrations

```bash
flask db migrate -m "description"   # Generate migration
flask db upgrade                    # Apply migrations
flask db downgrade                  # Rollback one migration
flask db current                    # Show current revision
flask db history                    # Show migration history
```

### Seeding Data

```python
# scripts/seed_data.py
from app import create_app
from app.extensions import db
from app.models import Quiz

app = create_app('development')
with app.app_context():
    quiz = Quiz(category="Python", title="Python Basics", total_questions=10)
    db.session.add(quiz)
    db.session.commit()
```

## Debugging

### Flask Shell

```bash
flask shell

>>> from app.models import User
>>> User.query.all()
>>> user = User.query.first()
>>> user.username
```

### Python Debugger

```python
import pdb; pdb.set_trace()  # Add breakpoint
```

### Logging

```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

## Commit Conventions

Format: `<type>(<scope>): <subject>`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructure
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```
feat(auth): add email verification
fix(quiz): prevent duplicate submissions
docs(api): update authentication endpoints
test(models): add user model tests
```

## Useful Commands

```bash
# Flask
flask run                          # Start dev server
flask routes                       # Show all routes
flask shell                        # Interactive shell

# Database
flask db upgrade                   # Apply migrations
flask db downgrade                 # Rollback
psql quiz_app_dev                  # Connect to DB

# Testing
pytest --cov=app                   # Run with coverage
pytest -x -v                       # Stop on fail, verbose
pytest tests/unit/test_models.py   # Specific file

# Formatting
black app/ tests/ scripts/         # Format code
isort app/ tests/ scripts/         # Sort imports
flake8 app/ tests/ scripts/        # Lint code

# Docker
docker-compose up                  # Start services
docker-compose logs -f web         # View logs
docker-compose exec web flask shell # Execute command
```

## Code Review Checklist

**Before submitting PR:**
- [ ] Tests pass locally
- [ ] Code formatted (Black, isort)
- [ ] No linting errors
- [ ] Tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow conventions

**When reviewing:**
- [ ] Follows style guide
- [ ] Tests are comprehensive
- [ ] No security issues
- [ ] Documentation updated
- [ ] CI passes

## Troubleshooting

**Import errors:** Activate venv (`source venv/bin/activate`)

**Database errors:** Reset DB (`rm quiz_app.db && flask db upgrade`)

**Port in use:** Kill process (`lsof -i :5000` then `kill -9 <PID>`)

**Tests failing:** Clear cache (`pytest --cache-clear`)

## Resources

- [API Documentation](API.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Architecture](ARCHITECTURE.md)
- [Flask Docs](https://flask.palletsprojects.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [pytest Docs](https://docs.pytest.org/)

## Getting Help

- Review documentation
- Search [GitHub Issues](https://github.com/your-username/production-quiz-app/issues)
- Create issue with `question` label
