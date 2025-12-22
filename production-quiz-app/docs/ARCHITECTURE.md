# Architecture Documentation

## System Overview

The Production Quiz App follows a layered architecture pattern with clear separation of concerns.

## High-Level Architecture

```
┌─────────────────┐
│  User/Browser   │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│     Nginx       │  Reverse Proxy, SSL, Static Files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Gunicorn      │  WSGI Server (4 workers)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Flask App     │  Application Layer
└─────┬─────┬─────┘
      │     │
      ▼     ▼
┌──────┐ ┌──────┐
│PostgreSQL│ Redis│  Data & Cache
└──────┘ └──────┘
```

## Technology Stack

**Backend Framework:**
- Flask 3.0.0 (Web framework)
- Gunicorn 21+ (WSGI server)
- SQLAlchemy 2.0 (ORM)
- Flask-Login (Session management)
- Flask-WTF (Forms & CSRF)
- Flask-Limiter (Rate limiting)

**Database:**
- PostgreSQL 15 (Primary database)
- Redis 7 (Cache & sessions)
- Alembic (Migrations)

**Testing:**
- pytest 7.4+ (Test framework)
- Factory Boy (Test fixtures)
- pytest-cov (Coverage)
- Faker (Test data)

**Security:**
- Werkzeug (Password hashing)
- Flask-CSRF (CSRF protection)
- Flask-Limiter (Rate limiting)

## Application Layers

### 1. Presentation Layer

**Routes/Blueprints (`app/routes/`):**
- Handle HTTP requests
- Route to appropriate services
- Return responses/templates

**Forms (`app/forms/`):**
- WTForms with validation
- CSRF token integration
- Custom validators

**Templates (`app/templates/`):**
- Jinja2 templates
- Responsive HTML/CSS
- Client-side JS

### 2. Business Logic Layer

**Services (`app/services/`):**
- Core business logic
- Orchestrate operations
- Independent of HTTP layer

Example: `AuthService`
- Registration logic
- Authentication logic
- Password reset workflows

### 3. Data Access Layer

**Models (`app/models/`):**
- SQLAlchemy ORM models
- Database schema definitions
- Relationships & constraints

**Key Models:**
- `User` - Authentication & profiles
- `Quiz` - Quiz metadata
- `Question` - Quiz questions
- `Attempt` - User quiz attempts
- `UserAnswer` - Individual answers

## Database Schema

### Entity Relationships

```
User (1) ─────── (*) Attempt (*) ─────── (1) Quiz
  │                    │                      │
  │                    │                      │
  └─── (*) UserAnswer (*)                (*) Question
            └─────────────────────────────────┘
```

### Key Tables

**users:**
- id, username, email, password_hash
- email_verified, verification_token
- failed_login_attempts, account_locked_until
- is_active, is_admin
- created_at, last_active

**quizzes:**
- id, category, title, description, icon
- total_questions, time_limit_minutes
- is_active, created_at

**questions:**
- id, quiz_id (FK)
- question, option_1-4, correct_answer
- difficulty, explanation, order_index

**attempts:**
- id, user_id (FK), quiz_id (FK)
- score, percentage, time_taken
- started_at, completed_at

**user_answers:**
- id, attempt_id (FK), question_id (FK)
- selected_answer, is_correct
- answered_at

### Indexes

- `users.username` (unique)
- `users.email` (unique)
- `quizzes.category` (index)
- `questions.quiz_id` (index)
- `attempts.user_id, quiz_id` (composite index)
- `user_answers.attempt_id` (index)

## Security Architecture

### Authentication Flow

```
1. User submits credentials
   ↓
2. AuthService.authenticate_user()
   - Find user by username/email
   - Check account not locked
   - Verify password hash
   - Reset failed attempts on success
   ↓
3. Flask-Login creates session
   - Session stored in Redis
   - Secure cookie sent to browser
   ↓
4. User authenticated
```

### Authorization

- `@login_required` decorator for protected routes
- `current_user` proxy for accessing logged-in user
- Role-based access via `is_admin` flag

### Password Security

- PBKDF2-SHA256 hashing (Werkzeug)
- Minimum 8 characters
- Complexity requirements (upper, lower, digits)
- Account lockout: 5 failed attempts = 15 min lock

### Session Security

- Server-side sessions in Redis
- HTTPOnly cookies (XSS protection)
- Secure flag (HTTPS only)
- SameSite=Lax (CSRF protection)
- 7-day session lifetime

### CSRF Protection

- WTForms CSRF tokens
- Per-session token generation
- Validated on all state-changing requests
- Token refresh on successful auth

### Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| /auth/register | 3 | 1 hour |
| /auth/login | 5 | 15 minutes |
| /auth/forgot-password | 3 | 1 hour |
| API endpoints | 100 | 1 hour |

## Data Flow Examples

### Registration Flow

```python
1. User → POST /auth/register
   {username, email, password}

2. RegistrationForm.validate()
   - Check field requirements
   - Custom validators

3. AuthService.register_user()
   - Check username uniqueness
   - Check email uniqueness
   - Hash password
   - Generate verification token
   - Create User record
   - Commit to database

4. Send verification email
   (email service integration)

5. Response → Success message
```

### Quiz Taking Flow

```python
1. User → POST /start {quiz_id}

2. Create Attempt record
   - user_id, quiz_id
   - started_at = now()

3. Load questions
   - Query by quiz_id
   - Shuffle order
   - Store in session

4. For each question:
   User → POST /submit {answer}
   - Store answer in session
   - Move to next question

5. After last question:
   - Calculate score
   - Create UserAnswer records
   - Update Attempt (score, completed_at)
   - Commit to database

6. Display results
```

## Caching Strategy

### Redis Usage

**Session Storage:**
- All user sessions
- TTL: 7 days
- Key format: `session:{session_id}`

**Rate Limiting:**
- Request counters
- TTL: Rate limit window
- Key format: `ratelimit:{identifier}`

**CSRF Tokens:**
- Per-session tokens
- TTL: Session lifetime
- Key format: `csrf:{session_id}`

### Future Caching

- Quiz metadata (5 min TTL)
- User statistics (10 min TTL)
- Leaderboard data (1 min TTL)

## Error Handling

### Exception Hierarchy

```python
class AppException(Exception):
    """Base application exception"""

class ValidationError(AppException):
    """Form/data validation errors"""

class AuthenticationError(AppException):
    """Authentication failures"""

class AuthorizationError(AppException):
    """Permission denied"""
```

### Error Responses

- **400**: Validation errors with details
- **401**: Authentication required
- **403**: Insufficient permissions
- **404**: Resource not found
- **429**: Rate limit exceeded
- **500**: Internal error (logged to Sentry)

## Design Patterns

### 1. Factory Pattern

**Application Factory:**
```python
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    return app
```

**Test Factories:**
```python
UserFactory()          # Create test user
QuizFactory()          # Create test quiz
AttemptFactory.create_completed()  # Completed attempt
```

### 2. Service Layer Pattern

```python
class AuthService:
    @staticmethod
    def register_user(username, email, password):
        # Business logic isolated from routes
        pass

    @staticmethod
    def authenticate_user(username_or_email, password):
        # Authentication logic
        pass
```

### 3. Blueprint Pattern

```python
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass
```

### 4. Decorator Pattern

```python
@login_required          # Authentication
@limiter.limit("5/15m")  # Rate limiting
@admin_required          # Authorization
def protected_route():
    pass
```

## Configuration Management

### Environment-Based Config

```python
class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'sqlite:///dev.db'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
```

### Environment Variables

- `.env.development` - Local development
- `.env.testing` - Test environment
- `.env.production` - Production secrets

## Performance Considerations

### Database Optimization

- Connection pooling (5 connections)
- Lazy loading relationships
- Indexed foreign keys
- Query result caching

### Application Optimization

- Static file caching (30 days)
- Gzip compression
- Minimal dependencies
- Efficient ORM queries

### Scalability

**Horizontal Scaling:**
- Stateless application
- Sessions in Redis
- Load balancer ready
- Multiple workers

**Vertical Scaling:**
- Adjustable worker count
- Database connection limits
- Memory limits

## Deployment Architecture

### Docker Container Structure

```yaml
services:
  web:
    image: quiz-app:latest
    depends_on: [postgres, redis]
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://...

  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    depends_on: [web]
    ports:
      - "80:80"
      - "443:443"
```

### Production Stack

```
Internet
   ↓
CloudFlare (CDN, DDoS)
   ↓
Nginx (Reverse Proxy, SSL)
   ↓
Gunicorn (4 workers)
   ↓
Flask Application
   ↓
PostgreSQL (AWS RDS) + Redis (ElastiCache)
```

## Monitoring & Observability

### Logging Levels

- **DEBUG**: Development only
- **INFO**: User actions (login, registration)
- **WARNING**: Failed attempts, anomalies
- **ERROR**: Exceptions, database errors
- **CRITICAL**: System failures

### Metrics (Future)

- Request latency (p50, p95, p99)
- Error rates by endpoint
- Database query performance
- Cache hit/miss ratios
- Active user sessions

### Health Checks

```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'database': check_database(),
        'redis': check_redis(),
        'timestamp': datetime.utcnow()
    }
```

## Testing Architecture

### Test Structure

```
tests/
├── conftest.py        # Fixtures
├── factories.py       # Test data factories
├── unit/             # Isolated unit tests
│   ├── test_models.py
│   └── test_services.py
└── integration/      # End-to-end tests
    └── test_auth_flow.py
```

### Test Database

- SQLite in-memory for speed
- PostgreSQL for integration tests
- Automatic rollback after each test

### Coverage Goals

- Overall: 80%+
- Critical paths: 90%+
- Security functions: 100%

## Future Enhancements

### Planned Features

- RESTful API with JWT
- Real-time leaderboards (WebSockets)
- Advanced analytics dashboard
- Mobile app support
- Multi-language support

### Technical Improvements

- GraphQL API
- Full-text search (Elasticsearch)
- Message queue (Celery)
- Microservices architecture
- Kubernetes deployment

## References

- [API Documentation](API.md)
- [Development Guide](DEVELOPMENT.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Contributing Guide](CONTRIBUTING.md)
