# Planning Agent Implementation Rules

**IMPORTANT:** These rules are for Planning Agents working on feature-level planning and breakdown. For implementation work, use Frontend/Backend Execute Agents.

## Feature Planning Process

For EACH new feature request, follow this exact sequence:

### Step 1: Requirements Analysis
- Review the user's feature request thoroughly
- Identify core functionality and acceptance criteria
- List all affected systems and integrations
- Note any dependencies on existing features

### Step 2: Architecture Planning
- Review planning patterns in planning-agent.md for similar features
- Design how this feature fits into existing project architecture
- Identify database changes, API endpoints, and UI components needed
- Plan integration points with existing services

### Step 3: Feature Breakdown
- Break feature into very small, independent chunks
- Each chunk should be completable in a single implementation session
- Define clear dependencies between chunks
- Ensure chunks can be tested and validated independently

### Step 4: Implementation Sequence
- Order chunks based on dependencies and logical flow
- Identify which chunks are frontend, backend, or both
- Plan testing strategy for each chunk
- Define integration points between chunks

### Step 5: Testing and Quality Strategy
- Define what tests are needed for each chunk
- Plan when tests should be written (before, during, or after implementation)
- Identify integration testing requirements
- Plan validation criteria for each chunk

### Step 6: Risk and Rollback Planning
- Identify potential risks and blockers
- Plan rollback strategy if feature needs to be reverted
- Document any breaking changes or migration requirements
- Plan communication and documentation needs

### Step 7: Feature Document Creation
- Create comprehensive feature document in `features/` folder
- Use incremented naming (feature-001.md, feature-002.md, etc.)
- Include all planning details in structured format
- Make document actionable for implementation agents

### Step 8: Implementation Readiness Verification
- Verify all chunks are small enough for single implementation sessions
- Ensure all dependencies are clearly documented
- Confirm testing strategy is complete and actionable
- Validate that feature integrates properly with existing patterns

## Feature Document Template

Create in `features/feature-XXX.md` with this exact format:

```markdown
# Feature XXX: [Feature Name]

## Requirements
- [List original user requirements]
- [Acceptance criteria]

## Architecture Design
- [How this feature fits into existing app patterns]
- [What components/services will be created/modified]
- [Integration points with existing systems]
- [Database changes required]

## Implementation Chunks

### Chunk 1: [Descriptive Name]
**Type:** Frontend/Backend/Both
**Dependencies:** None / Chunk X must be completed first
**Files to create/modify:**
- path/to/file1.tsx
- path/to/file2.ts
**Tests required:** Yes/No - [specific test requirements]
**Acceptance criteria:**
- [ ] Specific outcome 1
- [ ] Specific outcome 2

### Chunk 2: [Descriptive Name]
**Type:** Frontend/Backend/Both
**Dependencies:** Chunk 1 must be completed
**Files to create/modify:**
- path/to/file3.tsx
**Tests required:** Yes - [specific test requirements]
**Acceptance criteria:**
- [ ] Specific outcome 1

[Continue for all chunks...]

## Testing Strategy
- Unit tests: [when and what to test]
- Integration tests: [when and what to test]
- E2E tests: [when and what to test]

## Database Changes
- Migrations needed: [list migrations and timing]
- Data changes: [any data transformation needed]

## API Changes
- New endpoints: [list new endpoints]
- Modified endpoints: [list changes to existing endpoints]

## Integration Points
- Services affected: [list services and how they're affected]
- External systems: [any external system changes]

## Rollback Plan
- [How to undo this feature if needed]
- [Database rollback procedures]
- [Feature flag considerations]

## Documentation Updates
- [What documentation needs to be created/updated]

## Success Criteria
- [How to know when feature is complete]
- [Metrics or validation criteria]
```

## CRITICAL: Planning Agent Rules

- **NEVER implement code** - only create feature documents
- **NEVER skip the planning phase** - always create comprehensive feature documents
- **Break features into very small chunks** - each chunk should be completable in one session
- **Define clear dependencies** - make chunk ordering explicit
- **Plan testing strategy upfront** - don't leave testing as an afterthought
- **Follow project patterns** - use planning patterns from planning-agent.md
- **Create actionable documents** - implementation agents should be able to work directly from chunks
- **Verify integration points** - ensure feature works with existing systems
- **Plan for rollback** - always include rollback strategy
- **Document everything** - feature documents serve as implementation contracts

---

## Feature Planning Patterns - Production Quiz App (Flask)

### Aspect 1: Feature Planning Structure

1. **Phase-based feature organization**: Features in this project are organized into numbered phases (e.g., "Phase 1: Project Setup & Infrastructure", "Phase 3: Authentication & Security") with time estimates in days (e.g., "3-4 days", "4-5 days"). See `~/.claude/plans/memoized-cuddling-quiche.md` for the full implementation plan structure.

2. **Agent assignment per phase**: Each phase explicitly specifies which custom agent handles implementation (e.g., "Agent: Backend Agent", "Agent: Database Agent", "Agent: Backend Agent + Database Agent"). For example, Phase 2 (Database Migration) is assigned exclusively to Database Agent, while Phase 3 (Authentication & Security) is assigned to Backend Agent.

3. **Task-Critical Files-Deliverables structure**: Every phase follows this three-part breakdown: (1) numbered task list, (2) "Critical Files" section listing exact file paths to create/modify (e.g., `app/__init__.py`, `app/routes/auth.py`), (3) "Deliverables" section with checkboxes for completion tracking. See Phase 1 in the implementation plan as reference.

4. **Specification before implementation**: Features require upfront specification of file paths, line counts, and exact functionality before any code is written. For example, Phase 3 specifies "app/routes/auth.py - 200 lines" with 8 specific authentication routes listed, and "app/forms/auth_forms.py - 230 lines" with 6 specific form classes.

5. **Layered implementation order**: Features must be planned in this strict dependency order: (1) Database models (`app/models/`), (2) Services (`app/services/`), (3) Forms (`app/forms/`), (4) Routes (`app/routes/`), (5) Templates (`app/templates/`). Authentication feature in Phase 3 follows this exact pattern: User model enhancements → AuthService → Auth forms → Auth routes → Auth templates.

### Aspect 2: Database and Migration Patterns

6. **Model-first, migration-second approach**: Database changes are planned by first defining complete SQLAlchemy models with all fields, indexes, and constraints in `app/models/*.py`, then generating Alembic migrations with `flask db migrate`. The initial migration `d0a72a14ad60_initial_production_schema_with_enhanced_.py` was generated after all 5 model files (user.py, quiz.py, question.py, attempt.py, user_answer.py) were complete.

7. **Inline constraint definition in models**: All database constraints must be defined within model classes using `__table_args__` tuples containing db.CheckConstraint, db.Index, and db.UniqueConstraint objects. For example, User model in `app/models/user.py:62-67` defines 4 constraints: idx_user_username, idx_user_email, idx_user_last_active indexes, and check_failed_attempts_positive check constraint.

8. **Comprehensive check constraints for data validation**: Every numeric field with business rules must have check constraints defined. Examples from `migrations/versions/d0a72a14ad60_*.py`: percentage field has `check_percentage_valid` (0-100 range), score has `check_score_valid` (0 to total_questions), correct_answer has range constraint (0-3), and difficulty has enum constraint ('easy', 'medium', 'hard').

9. **Strategic index planning before implementation**: Indexes are planned based on expected query patterns: single-column indexes for WHERE clauses (e.g., `idx_user_email`), composite indexes for common query combinations (e.g., `idx_attempt_user_quiz` on user_id + quiz_id in attempts table), and indexes on foreign keys for join performance (quiz_id, user_id).

10. **Initial migration includes full production schema**: This project uses a single comprehensive initial migration instead of incremental migrations, containing all tables, indexes, constraints, and relationships. The migration `d0a72a14ad60_initial_production_schema_with_enhanced_.py` (250+ lines) creates all 5 tables (users, quizzes, questions, attempts, user_answers) with complete schema in one migration rather than iterative schema evolution.

### Aspect 3: Frontend-Backend Integration (Flask + Jinja2 Templates)

11. **Blueprint-based route organization**: Routes are organized into Flask Blueprints with dedicated blueprint files in `app/routes/` (e.g., `auth.py`, `dashboard.py`). Each blueprint is registered in `app/__init__.py` and handles related functionality. The auth blueprint (`auth_bp`) in `app/routes/auth.py:22` handles all authentication routes (/register, /login, /logout, /forgot-password, etc.).

12. **Form-Service-Template pattern**: Routes follow this exact pattern: (1) Import WTForm from `app/forms/`, (2) Import Service from `app/services/`, (3) Instantiate form in route, (4) Call service method with form.data, (5) Flash message, (6) Render template with form object. See `app/routes/auth.py:25-53` register() function for canonical example: RegistrationForm → AuthService.register_user() → flash() → render_template('auth/register.html', form=form).

13. **Service layer handles all business logic**: Routes MUST NOT contain business logic - only form handling, service method calls, flash messages, and template rendering. All authentication logic (password hashing, token generation, account lockout) is in `app/services/auth_service.py`, not in routes. Routes in `app/routes/auth.py` are 3-15 lines each, delegating to AuthService methods.

14. **Flask-WTF form rendering with CSRF**: All templates use WTForm field rendering with `{{ form.field_name(class="form-control") }}` syntax and include `{{ form.hidden_tag() }}` for CSRF protection. Error display uses standard pattern: `{% if form.field.errors %} {% for error in form.field.errors %} <div class="error">{{ error }}</div> {% endfor %} {% endif %}`. See `app/templates/auth/login.html:10-43` for canonical form template pattern.

15. **Template inheritance with base.html**: All templates extend `base.html` and override blocks (title, content). Templates are organized in subdirectories matching blueprints: `templates/auth/*.html` for auth blueprint routes, `templates/dashboard/*.html` for dashboard blueprint. Base template at `app/templates/base.html` contains common layout, navigation, and flash message display.

### Aspect 4: Testing Strategy and Timing

16. **Three-tier test structure with pytest**: Tests are organized into three directories: `tests/unit/` for isolated component tests (models, services), `tests/integration/` for workflow tests (auth flows, quiz flows), and `tests/e2e/` for complete user journey tests. Each test file follows naming convention `test_*.py` (e.g., `test_models.py`, `test_auth_flow.py`).

17. **Factory Boy for test data generation**: All test data is generated using Factory Boy factories defined in `tests/factories.py`. Each model has a base factory (UserFactory, QuizFactory) and specialized variants (AdminUserFactory, UnverifiedUserFactory, LockedUserFactory). Factories use `factory.Sequence()` for unique values, `factory.LazyAttribute()` for computed fields, and `factory.PostGenerationMethodCall('set_password')` for password hashing. See `tests/factories.py:30-93` for examples.

18. **Fixture-based test setup in conftest.py**: All test fixtures are centralized in `tests/conftest.py` with explicit scope definitions. Session-scoped fixtures (app) are created once per test run, function-scoped fixtures (client, db_session, sample_user) are recreated for each test. The `db_session` fixture at `tests/conftest.py:64-86` uses transaction rollback to ensure test isolation without database recreation.

19. **Database rollback for test isolation**: Tests use transaction-based rollback instead of recreating databases. The `db_session` fixture creates a nested transaction, runs the test, then rolls back all changes. Additionally, `reset_db_session` autouse fixture in `tests/conftest.py` clears all tables after each test by iterating `db.metadata.sorted_tables` in reverse order and executing `table.delete()`.

20. **Testing configuration separate from production**: Tests use dedicated "testing" configuration from `app/config.py` with in-memory SQLite database (`sqlite:///` or `sqlite:///:memory:`), CSRF disabled (`WTF_CSRF_ENABLED = False`), and `TESTING = True`. This configuration is activated in conftest.py app fixture with `create_app('testing')` at line 29.

### Aspect 5: Page and Route Creation

21. **Blueprint creation before registration**: New pages require creating a blueprint file in `app/routes/` first (e.g., `quiz.py` for quiz routes), defining the blueprint with `Blueprint('name', __name__)`, adding route decorators, then importing and registering in `app/__init__.py` register_blueprints() function. See `app/routes/dashboard.py:10` for blueprint definition and `app/__init__.py:94-100` for registration pattern.

22. **URL prefix assignment during blueprint registration**: Blueprints are registered with explicit url_prefix parameter in `app/__init__.py` register_blueprints() function. Auth blueprint uses `url_prefix="/auth"` making /auth/login, /auth/register routes. Dashboard blueprint has no prefix (url_prefix="") so / and /dashboard work. Pattern: `app.register_blueprint(blueprint_name, url_prefix="/prefix")`.

23. **Multiple route decorators for same function**: Routes can have multiple @blueprint.route() decorators to handle different URL patterns. Dashboard index() function at `app/routes/dashboard.py:13-14` has both `@dashboard_bp.route("/")` and `@dashboard_bp.route("/dashboard")` decorators, making it accessible at both root and /dashboard paths with no url_prefix.

24. **Template directory structure mirrors blueprint names**: Templates are organized in subdirectories matching blueprint names: `templates/auth/` for auth_bp routes, `templates/dashboard/` for dashboard_bp routes. Login route at `app/routes/auth.py:90` returns `render_template('auth/login.html')`, matching the auth blueprint name.

25. **Login protection with @login_required decorator**: Protected routes must have @login_required decorator from flask_login after route decorators and before function definition. Dashboard index at `app/routes/dashboard.py:13-16` shows correct order: @dashboard_bp.route(), then @login_required, then def index(). Routes without @login_required are public (login, register).

### Aspect 6: Service Integration Patterns

26. **Static method service classes**: Services are implemented as classes with all methods as @staticmethod decorators, not instance methods. AuthService in `app/services/auth_service.py:13` is a class with no __init__, no instance variables, and all methods decorated with @staticmethod. This pattern eliminates instantiation: call directly as AuthService.register_user(), not AuthService().register_user().

27. **Tuple return pattern for service methods**: Service methods return tuples of (result, error_message) where result is the object on success or None on failure, and error_message is None on success or error string on failure. See `app/services/auth_service.py:27-29` docstring: authenticate_user returns (User, None) on success or (None, "error message") on failure. Routes unpack with `user, error = AuthService.authenticate_user()`.

28. **Database transaction management in services**: All database operations in services follow this pattern: try block with db.session.add/commit, except block with db.session.rollback() and logging. Register_user in `app/services/auth_service.py:31-62` shows complete pattern: User creation in try, db.session.add(), db.session.commit(), then except with db.session.rollback() and current_app.logger.error().

29. **Service methods call model methods for domain logic**: Services orchestrate operations but delegate domain-specific logic to model methods. AuthService.register_user() calls user.set_password() and user.generate_verification_token() rather than implementing password hashing or token generation in the service. See `app/services/auth_service.py:46-49` where service delegates to User model methods.

30. **Flask current_app for logging in services**: Services use current_app.logger for logging, not module-level loggers. Import current_app from flask at top of service file, then use current_app.logger.info(), current_app.logger.error() for all logging. See `app/services/auth_service.py:7` import and `:55, :61, :111, :116` for usage in AuthService methods.

### Aspect 7: Email and Notification Integration

31. **Email configuration in BaseConfig with environment variables**: Email settings are defined in BaseConfig class in `app/config.py:52-58` using os.environ.get() for all values (MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER). This allows environment-specific configuration without code changes. Production uses real SMTP, development/testing can use logging-only placeholder.

32. **Placeholder email methods with TODO comments**: Email sending methods are implemented as placeholder stubs in services with TODO comments for production implementation. AuthService.send_verification_email() at `app/services/auth_service.py:315-341` logs the verification URL and includes commented example code for Flask-Mail integration, allowing development/testing without SMTP server while documenting production implementation path.

33. **Email methods return boolean success**: All email sending methods return boolean (True/False) to indicate success/failure, not tuple pattern. See send_verification_email() and send_password_reset_email() in `app/services/auth_service.py:315, 344` both return True. This allows callers to optionally check success without handling error messages (email failures shouldn't block user flows).

34. **Email methods are separate from business logic methods**: Email sending is implemented as separate @staticmethod methods (send_verification_email, send_password_reset_email) called by business logic methods, not inline. Register_user() in `app/services/auth_service.py:17` creates user and commits, then calling code invokes AuthService.send_verification_email(user) separately at `app/routes/auth.py:45`.

35. **Notification URLs logged to current_app.logger**: During development without real email, notification URLs are logged using current_app.logger.info() with descriptive messages including username. See `app/services/auth_service.py:331` logs "Verification URL for {user.username}: {verification_url}" so developers can access verification links during testing without checking email.

### Aspect 8: File Upload and Storage Integration

36. **Static files served from app/static/ directory**: Static assets (CSS, JS, images) are organized in `app/static/` with subdirectories for each type (css/, js/, images/). Flask serves these automatically at /static/ URL path. No custom static file serving configuration is needed - Flask's default static folder handling is used.

37. **No file upload functionality in current architecture**: This project does not implement file upload features because quiz functionality doesn't require user-uploaded files. If file upload is needed in future features (e.g., user profile photos, quiz attachments), it should follow this pattern: (1) Add UPLOAD_FOLDER and MAX_CONTENT_LENGTH to config.py, (2) Create upload service in app/services/, (3) Add WTForm FileField with validators, (4) Store file references in database, actual files in filesystem or S3.

38. **Future file storage should use environment-based configuration**: When file upload is added, storage backend (local filesystem vs S3/cloud) should be configured via environment variables in config.py, similar to email configuration. DevelopmentConfig uses local filesystem, ProductionConfig uses S3/cloud storage. This pattern is documented in `docs/ARCHITECTURE.md:540-556` Future Enhancements section.

39. **Static file caching configured in nginx**: Production static file serving is handled by nginx with long cache times (30 days) and immutable cache-control headers. See nginx configuration in `deployment/nginx/quiz_app.conf` for static file caching rules. Flask application never serves static files in production - nginx intercepts /static/ requests.

40. **No CDN integration in current deployment**: Static files are served directly from nginx without CDN. For future CDN integration (CloudFlare, CloudFront), static file URLs would need to be rewritten to CDN URLs using Flask's url_for() with _external=True parameter and CDN_DOMAIN configuration variable.

### Aspect 9: Background Job Integration

41. **No background job queue in current architecture**: This project does not implement Celery or any task queue system. All operations are synchronous and complete within HTTP request/response cycle. Email sending stubs (send_verification_email, send_password_reset_email) execute synchronously in `app/services/auth_service.py:315, 344` without queuing.

42. **Long-running operations handled synchronously**: Operations that would typically be backgrounded (email sending) are currently placeholder stubs that return immediately. When real email is implemented, these should remain synchronous for development/staging, only backgrounded in production. Pattern: if app.config['USE_TASK_QUEUE']: queue_task() else: execute_sync().

43. **Celery planned as future enhancement**: Background job infrastructure (Celery with Redis broker) is documented as planned enhancement in `docs/ARCHITECTURE.md:554` Technical Improvements section. When added, pattern should be: (1) Add celery to requirements/production.txt, (2) Create app/tasks/ directory with task modules, (3) Add CELERY_BROKER_URL to config, (4) Initialize Celery in app/extensions.py.

44. **Task queue integration should be opt-in per environment**: When Celery is added, it should be disabled in testing (tasks execute synchronously) and optional in development (USE_TASK_QUEUE=False in .env.development) to simplify local setup. Only production/staging require task queue running. TestingConfig should force CELERY_TASK_ALWAYS_EAGER=True for synchronous execution.

45. **Email sending is primary use case for background jobs**: When task queue is implemented, email operations (send_verification_email, send_password_reset_email) should be first tasks moved to background execution. Create app/tasks/email_tasks.py with @celery.task decorated functions that wrap existing email methods in app/services/auth_service.py without changing service method signatures.

### Aspect 10: Caching Strategy Integration

46. **Environment-based cache backend selection**: Cache backend is configured per environment in config.py: DevelopmentConfig and TestingConfig use SimpleCache (in-memory, process-local), StagingConfig and ProductionConfig use RedisCache with CACHE_REDIS_URL from environment. See `app/config.py:43, 99, 120, 142, 171` for cache type configuration pattern. SimpleCache is for development only - never use in production.

47. **Flask-Caching extension initialized in extensions.py**: Cache is initialized as module-level variable in `app/extensions.py:39` with `cache = Cache()`, then initialized with app in `app/__init__.py:81` via `cache.init_app(app)`. This pattern allows importing cache in any module without circular imports. Import with `from app.extensions import cache`.

48. **Redis used for infrastructure caching, not data caching**: Current implementation uses Redis exclusively for session storage, rate limiting counters, and CSRF tokens - not for application data caching (quiz results, user stats). Data caching patterns documented in `docs/ARCHITECTURE.md:286-290` as "Future Caching" with TTL specifications: quiz metadata (5 min), user statistics (10 min), leaderboard data (1 min).

49. **Explicit TTL required when adding cache decorators**: When adding @cache.cached() or @cache.memoize() decorators to functions, always specify timeout parameter explicitly, never rely on CACHE_DEFAULT_TIMEOUT (300 seconds). Pattern: @cache.cached(timeout=300, key_prefix='quiz_list') for consistency and documentation. Timeout should match business requirements in architecture docs.

50. **Cache health check in health endpoint**: Application health check at `app/__init__.py:148-150` tests cache connectivity with `cache.cache.get("health_check")` and reports status. This pattern should be followed for all external dependencies - health endpoint tests connectivity without affecting application functionality.

### Aspect 11: Security and Permissions Planning

51. **Rate limiting at route level with @limiter.limit decorator**: Rate limits are applied per-route using @limiter.limit() decorator with string format "N per TIME_UNIT". Auth routes in `app/routes/auth.py:26, 57, 117` show pattern: register is "3 per hour", login is "5 per 15 minutes", password reset is "3 per hour". Decorator goes between @route and function definition. More restrictive limits for sensitive operations.

52. **CSRF protection automatic via Flask-WTF**: All forms automatically have CSRF protection when using Flask-WTF - no decorator needed on routes. Forms include hidden CSRF token via `{{ form.hidden_tag() }}` in templates. CSRF is configured globally in `app/extensions.py:29` with `csrf = CSRFProtect()` and initialized in app factory. Only disabled in TestingConfig (`app/config.py:114` WTF_CSRF_ENABLED=False).

53. **Account lockout logic in User model, not service**: Failed login tracking and account lockout are implemented as User model methods (record_failed_login, is_account_locked, reset_failed_logins) in `app/models/user.py:158-187`, not in AuthService. Service calls user.record_failed_login() and user.is_account_locked(). Pattern: 5 failed attempts triggers 15-minute lockout, lockout time stored in account_locked_until field.

54. **Security headers applied via after_request hook**: Security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection) are defined in config.py SECURITY_HEADERS dict and applied to all responses via @app.after_request hook in `app/__init__.py:223-232`. This ensures headers on all responses without per-route configuration. Pattern: define in config, apply in factory.

55. **Permission checking with is_admin flag and decorators**: Authorization uses simple is_admin boolean flag on User model. For admin-only routes, pattern is: (1) Check current_user.is_admin in route function, (2) Return 403 if False, or (3) Create @admin_required decorator wrapping @login_required. No complex role/permission system - binary admin/non-admin distinction only. See User model `app/models/user.py:38` for is_admin field.

### Aspect 12: Configuration and Environment Planning

56. **Four-tier configuration inheritance with BaseConfig**: Configuration uses class inheritance with BaseConfig containing shared settings and four environment classes (DevelopmentConfig, TestingConfig, StagingConfig, ProductionConfig) inheriting and overriding. See `app/config.py:11-73` for BaseConfig with common settings, then `75-206` for environment-specific classes. Pattern: define once in BaseConfig, override only what differs per environment.

57. **Configuration selection via FLASK_ENV environment variable**: Active configuration is determined by FLASK_ENV environment variable, loaded via get_config() function in `app/config.py:222-234`. Function checks config_name parameter first, falls back to FLASK_ENV, defaults to "development". Set FLASK_ENV=production to load ProductionConfig. Application factory calls get_config() at `app/__init__.py:32`.

58. **Environment variables for secrets, not hardcoded values**: All sensitive values (SECRET_KEY, DATABASE_URL, REDIS_URL, MAIL_PASSWORD) use os.environ.get() with optional defaults only for development. BaseConfig pattern at `app/config.py:15, 53-58`: `SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"`. Production values MUST come from environment, never hardcoded.

59. **Production configuration validates required environment variables**: ProductionConfig has @classmethod init_app() method at `app/config.py:184-192` that validates required environment variables (DATABASE_URL, REDIS_URL, SECRET_KEY) and raises ValueError if missing. This ensures production deployment fails fast on misconfiguration. Other environments don't validate (allow defaults for easier development).

60. **Environment-specific defaults with progressive security**: Development uses permissive defaults (SQLite, SimpleCache, HTTP cookies) for easy local setup. Staging/Production require PostgreSQL, Redis, HTTPS cookies. Pattern: DevelopmentConfig has SESSION_COOKIE_SECURE=False (line 92), ProductionConfig has SESSION_COOKIE_SECURE=True (line 180). Security tightens from development → staging → production.

### Aspect 13: Documentation Requirements

61. **Two-tier documentation structure: root and docs/ directory**: Project documentation is split between root directory (operational docs: README.md, QUICKSTART.md, CICD.md, LINTING.md, DEPLOYMENT.md) and docs/ subdirectory (detailed technical docs: API.md, ARCHITECTURE.md, DEVELOPMENT.md, DEPLOYMENT.md, CONTRIBUTING.md). Root files are for quick reference, docs/ files are comprehensive guides. See `production-quiz-app/` root and `production-quiz-app/docs/` for current structure.

62. **README with badges, features, and quick start sections**: Main README.md follows standard structure: (1) badges (CI/CD, codecov, Python version, code style), (2) one-line description, (3) bullet-point features, (4) project structure diagram, (5) numbered quick start steps, (6) configuration details, (7) documentation links. See `production-quiz-app/README.md:1-100` for canonical pattern. Every feature mentioned must link to relevant documentation.

63. **Google-style docstrings for all public functions**: All service methods, model methods, and route functions require docstrings with three sections: (1) brief description, (2) Args section with parameter descriptions, (3) Returns section with return value structure. See `app/services/auth_service.py:17-29` register_user() docstring for canonical example: description → Args → Returns with tuple structure documented.

64. **Module-level docstrings describe file purpose**: Every Python file starts with module-level docstring in triple quotes describing what the module does. Pattern: brief one-line description, then optional longer explanation. Examples: `app/services/auth_service.py:1-5` "Authentication service with business logic. Handles user registration, login, password reset...", `app/routes/auth.py:1-4` "Authentication routes blueprint."

65. **Documentation updates required in same PR as code changes**: When features are implemented, documentation must be updated in the same PR, not deferred. Pattern: add feature → update API.md if new endpoints → update ARCHITECTURE.md if architecture changes → update README.md if setup changes. PROJECT_SUMMARY.md at `production-quiz-app/PROJECT_SUMMARY.md` documents completion status of phases, showing documentation was created alongside implementation in Phase 5.

### Aspect 14: Deployment and Release Planning

66. **Multi-stage Dockerfile for production optimization**: Production Dockerfile uses two-stage build at `production-quiz-app/Dockerfile:1-80`: Stage 1 (builder) installs build dependencies and creates venv, Stage 2 (runtime) copies only venv and application code with minimal runtime dependencies (libpq5, curl). Pattern eliminates build tools from production image, reducing size and attack surface. Builder stage creates /opt/venv, runtime stage copies it.

67. **Non-root user in production containers**: Dockerfile creates dedicated appuser at line 44 with `useradd --create-home --shell /bin/bash appuser`, switches to it at line 60 with `USER appuser`, and runs application as non-root. All application files owned by appuser via `--chown=appuser:appuser` flag at line 53. Never run production containers as root - security best practice.

68. **GitHub Actions CI/CD with sequential job dependencies**: CI pipeline at `.github/workflows/ci.yml` defines separate jobs for lint, security, test, build stages that can run in parallel or sequence. Test job includes services block (lines 88-110) for PostgreSQL and Redis containers. Pattern: independent jobs run parallel (lint, security), dependent jobs wait (deploy waits for test to pass).

69. **Deployment organized by target in deployment/ directory**: Deployment configurations separated by deployment method in `deployment/` subdirectories: docker/ for containerization, nginx/ for reverse proxy configs, systemd/ for service management. Each subdirectory is self-contained with necessary configs. Pattern keeps deployment concerns separated - don't mix Docker and systemd configs in same directory.

70. **Health check endpoint required for container orchestration**: Dockerfile includes HEALTHCHECK directive at lines 66-67 that calls /health endpoint every 30s. Application must implement /health endpoint that returns 200 when healthy, non-200 when unhealthy. See `app/__init__.py:118-160` for health check implementation testing database and cache connectivity. Container orchestrators (Docker, Kubernetes) use this for automatic restarts.

### Aspect 15: Rollback and Recovery Planning

71. **Automated database backups with retention policy**: Database backups are automated via backup_db.sh script at `production-quiz-app/scripts/backup_db.sh:1-250` with configurable retention (RETENTION_DAYS environment variable, default 7 days). Script creates timestamped compressed backups (quiz_app_backup_YYYYMMDD_HHMMSS.sql.gz), automatically deletes old backups, and logs all operations. Pattern: pg_dump with --clean --if-exists flags for safe restoration.

72. **Four-step rollback procedure documented**: Rollback follows explicit sequence in `docs/DEPLOYMENT.md:608-622`: (1) Stop application (systemctl stop), (2) Restore database from backup (psql < backup.sql), (3) Revert code (git checkout previous-commit), (4) Restart application (systemctl start). Database restoration MUST happen before code revert to maintain data consistency with previous code version.

73. **Alembic migrations support downgrade**: All database schema changes use Alembic migrations which generate both upgrade() and downgrade() functions. Rollback database schema with `flask db downgrade` command. Pattern documented in `docs/DEVELOPMENT.md:117` - downgrade rolls back one migration at a time. Never manually edit production database - always use migrations for schema changes and downgrades for rollback.

74. **Database backup verification before restoration**: Backup script at `scripts/backup_db.sh:120-140` includes backup verification step that tests backup integrity by attempting to read compressed file and checking file size > 0 bytes. Production restore procedure must verify backup file before restoration: test gunzip and check for SQL structure. Never restore unverified backup to production.

75. **Git tags required for production releases**: Production deployments must use git tags (e.g., v1.0.0, v1.1.0) not branch names, enabling precise rollback to specific versions with `git checkout v1.0.0`. Tag format: vMAJOR.MINOR.PATCH following semantic versioning. Rollback procedure in `docs/DEPLOYMENT.md:618` references "previous-stable-commit" which should be previous release tag.

### Aspect 16: Performance Considerations

76. **Gunicorn worker configuration based on CPU cores**: Production Dockerfile at `Dockerfile:70-80` configures Gunicorn with 4 workers, 2 threads per worker, gthread worker class. Pattern for worker count: (2 × CPU_CORES) + 1, so 4 workers assumes 2-core server. Worker class gthread allows handling concurrent requests with threads. Never use sync worker class with blocking operations (use gthread or gevent).

77. **Lazy loading for relationships by default**: SQLAlchemy relationships use lazy=True parameter to prevent N+1 query problems. User model at `app/models/user.py:59` defines `attempts = db.relationship("Attempt", backref="user", lazy=True)` preventing automatic loading of all attempts when querying user. For specific queries needing related data, use explicit joinedload or subqueryload, not eager loading by default.

78. **Database indexes on all foreign keys and query columns**: All foreign key columns have indexes defined in model __table_args__ or migration. User model has indexes on username, email, last_active. Attempts model has composite index on (user_id, quiz_id) for common query pattern. Pattern: add index to __table_args__ tuple in model definition, Alembic generates migration automatically. Never query on unindexed columns in production.

79. **Static file caching with long expiry**: Nginx configuration serves static files with 30-day cache expiry and immutable cache-control headers. Pattern documented in `docs/ARCHITECTURE.md:416` - static assets versioned via query strings or file hashes, allowing aggressive caching. Flask never serves static files in production - nginx intercepts /static/ requests before reaching application.

80. **Gunicorn worker-tmp-dir on shared memory**: Dockerfile Gunicorn configuration uses `--worker-tmp-dir /dev/shm` at line 75 to store worker temporary files in shared memory (RAM) instead of disk. This prevents disk I/O for worker heartbeats and temporary files. Pattern improves performance on containerized deployments where /tmp is overlay filesystem.

### Aspect 17: Monitoring and Observability

81. **Environment-based logging levels**: Logging level configured per environment in config.py: DevelopmentConfig uses DEBUG, StagingConfig uses INFO, ProductionConfig uses WARNING. See `app/config.py:96, 154, 204` for LOG_LEVEL configuration. Application logger reads config in `app/__init__.py:165` with `log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))`. Never log DEBUG level in production - sensitive data exposure risk.

82. **Rotating file handler for production logs**: Production logging uses RotatingFileHandler at `app/__init__.py:180-190` with max size LOG_MAX_BYTES (10MB) and LOG_BACKUP_COUNT (10 files) from config. Pattern prevents disk space exhaustion from unbounded log growth. Log files rotate automatically when size exceeded: app.log → app.log.1 → app.log.2 → ... → app.log.10, oldest deleted.

83. **Sentry integration for error tracking with sampling**: Sentry initialized in `app/__init__.py:236-251` only if SENTRY_DSN configured and not testing. Uses FlaskIntegration, traces_sample_rate=0.1 (10% of transactions), profiles_sample_rate=0.1 for profiling. Pattern: conditional initialization allows development/testing without Sentry, production with error tracking. Environment tag enables filtering errors by environment in Sentry dashboard.

84. **Health check endpoint tests external dependencies**: Health endpoint at `app/__init__.py:118-160` returns JSON with status, timestamp, service name, version, and connectivity status for database and cache. Pattern: try connecting to each service, set status to "healthy" only if all pass, "unhealthy" if any fail. Load balancers and monitoring tools query /health every 30-60s to detect failures and trigger alerts.

85. **Structured logging with contextual information**: All log statements use current_app.logger with contextual information - username, operation, timing. Pattern at `app/services/auth_service.py:55, 111`: `current_app.logger.info(f"User logged in: {user.username}")` includes specific user context. Avoid generic logs like "operation succeeded" - always include identifiers (user_id, quiz_id, attempt_id) for debugging and audit trails.

