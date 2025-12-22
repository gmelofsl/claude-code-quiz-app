# Contributing to Production Quiz App

Thank you for your interest in contributing to the Production Quiz App! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. We pledge to:

- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Expected Behavior

- Be respectful and professional in all interactions
- Provide constructive feedback
- Help others learn and grow
- Credit others for their contributions
- Report security issues responsibly

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Trolling, insulting comments, or personal attacks
- Publishing others' private information
- Spam or irrelevant content
- Any conduct that would be inappropriate in a professional setting

### Enforcement

Violations of the Code of Conduct should be reported to the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.9+** installed
- **PostgreSQL 15+** (for database testing)
- **Redis 7+** (for session/cache testing)
- **Git** installed and configured
- **GitHub account**

### Setting Up Development Environment

**1. Fork the Repository**

Click the "Fork" button on GitHub to create your own copy.

**2. Clone Your Fork**

```bash
git clone https://github.com/YOUR-USERNAME/production-quiz-app.git
cd production-quiz-app
```

**3. Add Upstream Remote**

```bash
git remote add upstream https://github.com/ORIGINAL-OWNER/production-quiz-app.git
```

**4. Create Virtual Environment**

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**5. Install Dependencies**

```bash
pip install -r requirements/development.txt
```

**6. Set Up Environment Variables**

```bash
cp .env.example .env.development
# Edit .env.development with your local configuration
```

**7. Initialize Database**

```bash
flask db upgrade
python scripts/seed_data.py
```

**8. Install Pre-Commit Hooks**

```bash
pre-commit install
```

**9. Verify Setup**

```bash
# Run tests
pytest

# Start development server
flask run
```

Visit http://localhost:5000 to verify the application works.

---

## Development Workflow

### Branching Strategy

We follow **Git Flow** branching model:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `fix/*` - Bug fixes
- `hotfix/*` - Critical production fixes
- `docs/*` - Documentation updates

### Creating a Branch

**For new features:**
```bash
git checkout develop
git pull upstream develop
git checkout -b feature/your-feature-name
```

**For bug fixes:**
```bash
git checkout develop
git pull upstream develop
git checkout -b fix/bug-description
```

**For documentation:**
```bash
git checkout develop
git pull upstream develop
git checkout -b docs/update-description
```

### Branch Naming Conventions

- Use lowercase with hyphens
- Be descriptive but concise
- Include ticket number if applicable

**Examples:**
- `feature/timed-quiz-mode`
- `fix/login-redirect-loop`
- `docs/api-authentication`
- `hotfix/security-vulnerability-123`

### Making Changes

**1. Write Code**

Follow the [Coding Standards](#coding-standards) section below.

**2. Write Tests**

All new features and bug fixes **must** include tests. See [Testing Requirements](#testing-requirements).

**3. Run Tests Locally**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py
```

**4. Format Code**

```bash
# Auto-format with Black and isort
black app/ tests/ scripts/
isort app/ tests/ scripts/

# Or use the convenience script
./scripts/format.sh  # Linux/Mac
scripts\format.bat   # Windows
```

**5. Lint Code**

```bash
# Check code quality
flake8 app/ tests/ scripts/

# Run all linting checks
./scripts/lint.sh  # Linux/Mac
scripts\lint.bat   # Windows
```

**6. Commit Changes**

See [Commit Guidelines](#commit-guidelines) below.

---

## Coding Standards

### Style Guide

We follow **PEP 8** with the following tools:

- **Black** - Code formatter (line-length: 100)
- **isort** - Import sorting (Black-compatible)
- **Flake8** - Linter (max-complexity: 10)

**Key Rules:**

- **Line length:** 100 characters
- **Indentation:** 4 spaces (no tabs)
- **Quotes:** Double quotes for strings
- **Naming:**
  - Classes: `PascalCase` (e.g., `UserModel`, `AuthService`)
  - Functions/variables: `snake_case` (e.g., `get_user`, `user_id`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_ATTEMPTS`)
  - Private: Prefix with `_` (e.g., `_internal_method`)

### Code Organization

**Application Structure:**

```python
app/
├── __init__.py          # Application factory
├── config.py            # Configuration classes
├── extensions.py        # Flask extensions
├── models/              # Database models
│   ├── __init__.py
│   ├── user.py
│   └── quiz.py
├── routes/              # Blueprints (controllers)
│   ├── __init__.py
│   └── auth.py
├── services/            # Business logic
│   ├── __init__.py
│   └── auth_service.py
├── forms/               # WTForms
│   └── auth_forms.py
└── utils/               # Helper functions
    └── validators.py
```

**Separation of Concerns:**

- **Routes:** HTTP request/response handling only
- **Services:** Business logic, orchestration
- **Models:** Data structure, database operations
- **Forms:** Input validation
- **Utils:** Reusable helper functions

### Documentation

**Docstrings (Google Style):**

```python
def authenticate_user(username: str, password: str) -> Tuple[Optional[User], Optional[str]]:
    """
    Authenticate user by username and password.

    Args:
        username: Username or email address
        password: Plain text password to verify

    Returns:
        Tuple of (user object, error message)
        If successful: (User, None)
        If failed: (None, "error message")

    Raises:
        ValueError: If username or password is empty

    Example:
        >>> user, error = authenticate_user("john", "SecurePass123")
        >>> if user:
        ...     print(f"Welcome {user.username}")
    """
    pass
```

**Required for:**
- All public functions and methods
- All classes
- Complex algorithms or logic

**Not required for:**
- Private methods (optional)
- Simple getters/setters
- Self-explanatory code

### Type Hints

Use type hints for all function signatures:

```python
from typing import Optional, List, Dict, Tuple

def get_user_stats(user_id: int) -> Dict[str, float]:
    """Get statistics for a user."""
    pass

def find_users(query: str, limit: int = 10) -> List[User]:
    """Search for users."""
    pass
```

### Error Handling

**Use specific exceptions:**

```python
# Good
try:
    user = User.query.get_or_404(user_id)
except NotFound:
    return {"error": "User not found"}, 404

# Bad
try:
    user = User.query.get_or_404(user_id)
except Exception:
    pass
```

**Always provide context:**

```python
# Good
raise ValueError(f"Invalid quiz_id: {quiz_id}. Must be positive integer.")

# Bad
raise ValueError("Invalid input")
```

---

## Testing Requirements

### Coverage Requirements

- **Minimum overall coverage:** 80%
- **Critical paths (auth, quiz logic):** 90%+
- **Security functions:** 100%

### Test Types

**1. Unit Tests** (`tests/unit/`)

Test individual functions and methods in isolation.

```python
# tests/unit/test_models.py
def test_user_set_password(app):
    """Test User.set_password() method."""
    with app.app_context():
        user = UserFactory()
        user.set_password("TestPass123")
        assert user.check_password("TestPass123")
        assert not user.check_password("WrongPass")
```

**2. Integration Tests** (`tests/integration/`)

Test complete workflows and interactions between components.

```python
# tests/integration/test_auth_flow.py
def test_registration_flow(client):
    """Test complete registration workflow."""
    # Register user
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'TestPass123',
        'confirm_password': 'TestPass123'
    })
    assert response.status_code == 302

    # Verify user created
    user = User.query.filter_by(username='newuser').first()
    assert user is not None
    assert user.email_verified is False
```

**3. End-to-End Tests** (`tests/e2e/`)

Test complete user journeys from start to finish.

```python
# tests/e2e/test_user_journey.py
def test_complete_quiz_journey(client):
    """Test: Register → Login → Take Quiz → View Results → History."""
    # Implementation
    pass
```

### Test Guidelines

**Do:**
- Test happy path and edge cases
- Use descriptive test names
- Use factories for test data (`tests/factories.py`)
- Clean up after tests (fixtures handle this)
- Test error conditions
- Mock external services (email, APIs)

**Don't:**
- Test framework code (Flask, SQLAlchemy)
- Write tests that depend on each other
- Hardcode test data (use factories)
- Skip tests (mark as `@pytest.mark.skip` with reason)
- Test implementation details

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_models.py

# Specific test function
pytest tests/unit/test_models.py::test_user_set_password

# With coverage report
pytest --cov=app --cov-report=html

# Stop on first failure
pytest -x

# Verbose output
pytest -v

# Show print statements
pytest -s
```

---

## Commit Guidelines

We follow **Conventional Commits** specification.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Example:**

```
feat(auth): add email verification workflow

Implement email verification for new user registrations:
- Generate unique verification tokens
- Send verification emails via SMTP
- Add /auth/verify/<token> route
- Update User model with email_verified field

Closes #42
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(quiz): add timed quiz mode` |
| `fix` | Bug fix | `fix(auth): resolve login redirect loop` |
| `docs` | Documentation | `docs(api): update authentication endpoints` |
| `style` | Formatting, no code change | `style: apply Black formatting` |
| `refactor` | Code restructure, no behavior change | `refactor(services): extract quiz logic` |
| `test` | Add or update tests | `test(models): add User model tests` |
| `chore` | Maintenance, dependencies | `chore: update Flask to 3.0.1` |
| `perf` | Performance improvement | `perf(db): add indexes to queries` |
| `ci` | CI/CD changes | `ci: add codecov integration` |
| `build` | Build system changes | `build: update Docker configuration` |

### Scope

Optional but recommended. Indicates what part of codebase is affected:

- `auth` - Authentication
- `quiz` - Quiz functionality
- `models` - Database models
- `routes` - Route handlers
- `services` - Business logic
- `tests` - Test suite
- `docs` - Documentation
- `ci` - CI/CD pipeline

### Subject

- Use imperative mood ("add feature" not "added feature")
- Lowercase first letter
- No period at the end
- Maximum 72 characters

### Body (Optional)

- Explain **what** and **why**, not how
- Use bullet points for multiple changes
- Wrap at 72 characters

### Footer (Optional)

- Reference issues: `Closes #123`, `Fixes #456`, `Refs #789`
- Breaking changes: `BREAKING CHANGE: description`

### Examples

**Good commits:**

```
feat(auth): add password reset functionality

fix(quiz): prevent duplicate question submissions

docs: update deployment guide for Docker

test(auth): add integration tests for login flow

refactor(services): extract email sending to service layer
```

**Bad commits:**

```
Update stuff
Fixed bug
WIP
asdf
Commit
```

---

## Pull Request Process

### Before Submitting

**Checklist:**

- [ ] Code follows style guide (Black, isort, Flake8 pass)
- [ ] All tests pass locally (`pytest`)
- [ ] Coverage meets requirements (80%+)
- [ ] New tests added for new features/fixes
- [ ] Documentation updated (docstrings, README, guides)
- [ ] Commit messages follow conventions
- [ ] Branch is up-to-date with `develop`
- [ ] No merge conflicts

### Submitting Pull Request

**1. Push to Your Fork**

```bash
git push origin feature/your-feature-name
```

**2. Create Pull Request on GitHub**

- **Base branch:** `develop` (or `main` for hotfixes)
- **Compare branch:** Your feature branch
- **Title:** Clear, descriptive (follows commit convention)
- **Description:** Use the PR template

**PR Title Format:**

```
feat(auth): add email verification
fix(quiz): resolve duplicate submissions
docs: update API documentation
```

**PR Description Template:**

```markdown
## Description
Brief description of changes and motivation.

## Changes Made
- Added email verification workflow
- Updated User model with email_verified field
- Created verification email template

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [x] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
Describe how you tested the changes:
- Unit tests added for User.verify_email()
- Integration tests for /auth/verify/<token> route
- Manual testing: verified email workflow end-to-end

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [x] Code follows style guide
- [x] Tests pass locally
- [x] Documentation updated
- [x] Commit messages follow conventions

## Related Issues
Closes #42
```

### Review Process

**What Reviewers Look For:**

1. **Code Quality:**
   - Follows style guide
   - Clean, readable code
   - Proper error handling
   - No code smells

2. **Testing:**
   - Adequate test coverage
   - Tests are meaningful
   - Edge cases covered

3. **Security:**
   - No SQL injection vulnerabilities
   - No XSS vulnerabilities
   - Proper input validation
   - CSRF protection in place

4. **Performance:**
   - No N+1 query problems
   - Efficient algorithms
   - Proper indexing

5. **Documentation:**
   - Code is documented
   - User-facing docs updated
   - API changes documented

**Addressing Feedback:**

- Respond to all comments
- Make requested changes
- Push additional commits (don't force-push during review)
- Mark conversations as resolved when addressed
- Request re-review when ready

### Merging

**Requirements:**
- At least 1 approval from maintainer
- All CI checks passing
- No merge conflicts
- Branch up-to-date with base

**Merge Strategy:**
- Feature branches: Squash and merge
- Hotfixes: Merge commit
- Release branches: Merge commit

---

## Issue Guidelines

### Before Creating an Issue

- Search existing issues (open and closed)
- Check documentation
- Try latest version
- Verify it's reproducible

### Bug Reports

**Use the bug report template:**

```markdown
## Bug Description
Clear description of the bug.

## Steps to Reproduce
1. Go to '/auth/login'
2. Enter username 'test'
3. Click 'Login'
4. See error

## Expected Behavior
Should redirect to dashboard.

## Actual Behavior
Shows 500 error page.

## Environment
- OS: Ubuntu 22.04
- Python: 3.11.2
- Browser: Chrome 120
- Database: PostgreSQL 15.4

## Error Logs
```
[Paste error logs here]
```

## Additional Context
Screenshots, related issues, etc.
```

### Feature Requests

**Use the feature request template:**

```markdown
## Feature Description
Clear description of the proposed feature.

## Use Case
Explain why this feature is needed and who benefits.

## Proposed Solution
How you think it could be implemented.

## Alternatives Considered
Other approaches you've thought about.

## Additional Context
Mockups, examples from other apps, etc.
```

### Issue Labels

| Label | Description |
|-------|-------------|
| `bug` | Something isn't working |
| `feature` | New feature request |
| `enhancement` | Improvement to existing feature |
| `documentation` | Documentation improvements |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention needed |
| `question` | Further information requested |
| `wontfix` | This will not be worked on |
| `duplicate` | This issue already exists |
| `security` | Security vulnerability |
| `performance` | Performance-related |

---

## Community

### Getting Help

- **Documentation:** Check [docs/](../docs/) folder
- **Issues:** Search GitHub issues
- **Discussions:** Use GitHub Discussions for questions
- **Email:** [Maintainer email if applicable]

### Communication Channels

- **GitHub Issues:** Bug reports, feature requests
- **GitHub Discussions:** General questions, ideas
- **Pull Requests:** Code review discussions

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in commit messages

---

## Development Tips

### Useful Commands

```bash
# Database
flask db migrate -m "description"   # Create migration
flask db upgrade                    # Apply migrations
flask db downgrade                  # Rollback
flask shell                         # Interactive shell

# Testing
pytest -k "test_auth"               # Run tests matching pattern
pytest --lf                         # Run last failed tests
pytest --sw                         # Stop on first failure, continue next run

# Debugging
FLASK_DEBUG=1 flask run             # Run with debugger
python -m pdb app.py                # Run with Python debugger
import pdb; pdb.set_trace()         # Breakpoint in code

# Code Quality
black --check app/                  # Check formatting (no changes)
isort --check-only app/             # Check imports (no changes)
flake8 app/ --statistics            # Show linting statistics
```

### IDE Setup

**VS Code:**

Install extensions:
- Python
- Pylance
- Black Formatter
- isort
- Flake8

**Settings (`.vscode/settings.json`):**

```json
{
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

**PyCharm:**

- Settings → Tools → Black → Enable
- Settings → Tools → File Watchers → Add isort
- Settings → Editor → Inspections → Enable Flake8

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

## Questions?

If you have questions not covered in this guide:

1. Check the [documentation](../docs/)
2. Search [existing issues](../../issues)
3. Create a new issue with the `question` label
4. Reach out to maintainers

Thank you for contributing to Production Quiz App! 🎉
