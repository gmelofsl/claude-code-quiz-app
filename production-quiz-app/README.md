# Production Quiz App

[![CI/CD Pipeline](https://github.com/YOUR-USERNAME/production-quiz-app/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/YOUR-USERNAME/production-quiz-app/actions)
[![codecov](https://codecov.io/gh/YOUR-USERNAME/production-quiz-app/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR-USERNAME/production-quiz-app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready Flask-based educational platform for testing knowledge of AI software development concepts.

## Features

- **Secure Authentication**: Email + password with Argon2 hashing, email verification, password reset
- **PostgreSQL Database**: Production-grade database with Alembic migrations
- **Redis Caching**: Server-side sessions and caching layer
- **Security**: CSRF protection, rate limiting, security headers, input validation
- **Testing**: 80%+ code coverage with unit, integration, and E2E tests
- **Deployment Ready**: Docker, Docker Compose, Nginx, CI/CD pipeline
- **Error Tracking**: Sentry integration for production monitoring

## Project Structure

```
production-quiz-app/
├── app/                    # Application code
│   ├── models/            # Database models
│   ├── routes/            # Flask blueprints
│   ├── services/          # Business logic
│   ├── forms/             # WTForms with validation
│   ├── utils/             # Helper utilities
│   ├── templates/         # Jinja2 templates
│   └── static/            # CSS, JS, images
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/              # End-to-end tests
├── migrations/            # Alembic migrations
├── scripts/               # Utility scripts
├── deployment/            # Docker, Nginx configs
├── requirements/          # Split requirements files
└── .github/workflows/     # CI/CD pipelines
```

## Quick Start

### 1. Clone and Setup

```bash
cd production-quiz-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements/development.txt
```

### 2. Configure Environment

```bash
cp .env.example .env.development
# Edit .env.development with your settings
```

### 3. Initialize Database

```bash
# Run migrations
flask db upgrade

# Seed database (if seed script exists)
python scripts/seed_data.py
```

### 4. Run Development Server

```bash
python run.py
```

Visit: http://localhost:5000

## Configuration

### Environments

The app supports 4 environments:
- **development**: SQLite, debug enabled, simple cache
- **testing**: Separate test database, CSRF disabled
- **staging**: PostgreSQL, Redis, production-like
- **production**: PostgreSQL, Redis, strict security

Set environment with:
```bash
export FLASK_ENV=development  # or staging, production
```

### Environment Variables

Required variables (see `.env.example`):
- `SECRET_KEY`: Cryptographic secret (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis connection string (staging/production)

Optional variables:
- `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`: Email configuration
- `SENTRY_DSN`: Error tracking
- `LOG_LEVEL`, `LOG_FILE`: Logging configuration

## Development

### Install Dependencies

```bash
# Base + development tools
pip install -r requirements/development.txt
```

### Run Tests

```bash
# All tests with coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/unit/test_models.py

# With verbose output
pytest -v
```

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

### Code Quality & Linting

**Quick Commands:**
```bash
# Run all checks
./scripts/lint.sh          # Linux/Mac
scripts\lint.bat           # Windows

# Auto-fix formatting issues
./scripts/format.sh        # Linux/Mac
scripts\format.bat         # Windows
```

**Individual Tools:**
```bash
# Code formatting
black app/ tests/

# Import sorting
isort app/ tests/

# Linting
flake8 app/ tests/

# Security scanning
bandit -r app/

# Type checking
mypy app/
```

**Pre-commit Hooks (Optional):**
```bash
# Install hooks
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

See [LINTING.md](LINTING.md) for detailed linting guide.

## Production Deployment

### Docker (Recommended)

**Quick Start:**
```bash
# Configure environment
cp .env.example .env.production
# Edit .env.production with production values

# Start all services (PostgreSQL, Redis, Flask, Nginx)
docker-compose up -d

# Run migrations
docker-compose exec web flask db upgrade

# Seed database
docker-compose exec web python scripts/seed_data.py

# View logs
docker-compose logs -f
```

**Services:**
- **Web**: Flask app with Gunicorn (port 8000)
- **PostgreSQL**: Database (port 5432)
- **Redis**: Cache and sessions (port 6379)
- **Nginx**: Reverse proxy with SSL (ports 80, 443)

**Health Check:**
```bash
curl http://localhost:8000/health
```

### Manual Deployment

1. Set up PostgreSQL and Redis
2. Configure environment variables
3. Run migrations: `flask db upgrade`
4. Start with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 run:app
   ```
5. Configure Nginx as reverse proxy

See `DEPLOYMENT.md` for detailed instructions.

## Testing

### Run Test Suite

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html --cov-report=term

# Specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

### Coverage Goals

- Overall: 80%+
- Critical paths (auth, quiz logic): 90%+
- Security functions: 100%

## Security

- Argon2 password hashing
- CSRF protection on all forms
- Rate limiting on sensitive endpoints
- Redis-backed server-side sessions
- Security headers (HSTS, CSP, X-Frame-Options, etc.)
- Input validation and sanitization
- SQL injection prevention (ORM)

## Architecture

### Application Factory Pattern

The app uses Flask's application factory pattern for:
- Multiple configurations (dev/test/prod)
- Better testability
- Blueprint registration
- Extension initialization

### Service Layer

Business logic is separated into service modules:
- `auth_service.py`: Authentication logic
- `quiz_service.py`: Quiz taking logic
- `stats_service.py`: Statistics calculations
- `cache_service.py`: Redis caching

### Database Models

- `User`: Enhanced with password hashing, email verification
- `Quiz`: Quiz categories and metadata
- `Question`: Questions with difficulty levels
- `Attempt`: Quiz attempts with scoring
- `UserAnswer`: Individual question answers

## Custom Agents

Use specialized agents during development:

```bash
# Backend features
/backend-agent [task description]

# Database operations
/database-agent [task description]

# Quiz content
/quiz-content-agent [task description]
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

### Core Documentation

- **[API Documentation](docs/API.md)** - Complete API reference with examples
  - Authentication endpoints (register, login, email verification, password reset)
  - Quiz endpoints (dashboard, start quiz, submit answers)
  - Request/response formats and error codes
  - Rate limiting and security details
  - Code examples (Python, JavaScript, cURL)

- **[Architecture Documentation](docs/ARCHITECTURE.md)** - System design and patterns
  - High-level architecture diagram
  - Technology stack overview
  - Application layers (Presentation, Business Logic, Data Access)
  - Database schema with ERD
  - Security architecture and authentication flow
  - Caching strategy and performance considerations
  - Design patterns used throughout the app

- **[Development Guide](docs/DEVELOPMENT.md)** - Developer workflow and standards
  - Quick start instructions
  - Coding standards (PEP 8, Black, isort)
  - Testing guide with examples
  - Database migration commands
  - Debugging tips and Flask shell usage
  - Useful development commands

- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment instructions
  - Docker deployment (recommended approach)
  - Manual deployment with systemd
  - Cloud platforms (AWS, Heroku, DigitalOcean, GCP)
  - Database migration strategies
  - Monitoring and troubleshooting
  - Security checklist and backup strategies

- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute
  - Code of Conduct
  - Development workflow and branching strategy
  - Coding standards and style guide
  - Testing requirements (80%+ coverage)
  - Commit message conventions
  - Pull request process
  - Issue guidelines

### Additional Documentation

- **[Linting Guide](LINTING.md)** - Code quality and formatting
  - Black, isort, Flake8, Bandit, mypy setup
  - Pre-commit hooks configuration
  - IDE integration guides
  - Troubleshooting common issues

- **[CI/CD Documentation](CICD.md)** - Continuous integration and deployment
  - GitHub Actions workflows
  - Pipeline stages and jobs
  - Automated testing and deployment
  - Troubleshooting CI/CD issues

- **[Quick Start Guide](.github/CICD-QUICK-START.md)** - CI/CD setup
  - GitHub Secrets configuration
  - Branch protection setup
  - Badge URL updates

### Getting Started

New to the project? Start here:

1. Read the [Development Guide](docs/DEVELOPMENT.md) for setup instructions
2. Review the [Architecture Documentation](docs/ARCHITECTURE.md) to understand the system
3. Check the [Contributing Guide](docs/CONTRIBUTING.md) before making changes
4. Refer to the [API Documentation](docs/API.md) when working with endpoints

## License

[Your License Here]

## Contributing

We welcome contributions! Please read our [Contributing Guide](docs/CONTRIBUTING.md) for details on:

- Code of Conduct
- Development workflow and branching strategy
- Coding standards and testing requirements
- How to submit pull requests
- Issue reporting guidelines

Before submitting a PR, ensure:
- All tests pass (`pytest`)
- Code is formatted (`black`, `isort`)
- Linting passes (`flake8`)
- Coverage meets requirements (80%+)
- Documentation is updated

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for complete guidelines.
