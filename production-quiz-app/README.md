# Production Quiz App

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

### Code Quality

```bash
# Format code
black app tests

# Sort imports
isort app tests

# Lint
flake8 app tests
```

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

## License

[Your License Here]

## Contributing

[Contributing Guidelines]
