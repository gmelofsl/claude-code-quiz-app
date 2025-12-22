# Backend Agent Implementation Rules

**IMPORTANT:** These rules are for Backend Execute Agents working on specific chunks from a feature plan. For new features or complex changes, use the Plan Agent first (see ../../workflows/feature-flow.md).

## Per-File Implementation Loop

For EACH individual file, follow this exact sequence:

### Step 1: Pattern Check
- Review the pattern rules in backend-patterns.md for this file type
- Identify which specific rules apply to this file

### Step 2: Similar Files Analysis
- Find 3-5 existing files of the same type in the project
- Study their structure, naming, and implementation patterns
- Note the exact conventions they follow
- **NEVER assume modules/endpoints exist - always verify exact names and paths**

### Step 3: Implement File
- **Check that all imports/modules you want to use actually exist first**
- Create the single file following the patterns discovered
- Use the exact naming, structure, and style from similar files
- **Verify module names and import paths before using them**

### Step 4: Verify Pattern Match
- Compare the new file against the pattern rules in backend-patterns.md
- Ensure it follows the same conventions as existing similar files
- **Verify file is in the correct folder** following project structure
- **Verify all imports are correct** and follow project import patterns
- Fix any deviations immediately

### Step 5: Verify Types
- **Use VSCode MCP server getDiagnostics if available** for efficient type checking
- If MCP not available, check that types compile correctly
- Ensure TypeScript (if used) passes for this file
- Fix any type errors

### Step 6: Write Test (MANDATORY if project has tests)
- **NEVER skip this step** - always check if similar files have tests
- If project has tests for similar files, **YOU MUST write test for this file**
- Follow the same testing patterns used in the project
- **Run the test for THIS FILE ONLY** to verify it passes

### Step 7: Final Validation, Verification and Documentation
- **Use VSCode MCP server getDiagnostics if available** for final type/lint checking
- **Run linting tools on this single file** - must pass
- **Run type checking on this single file** - must pass
- Verify the file integrates with existing code
- **If feature requires permissions:** Check if existing permission applies or ask user if new permission needed
- **Verify pattern compliance:** Confirm this file follows ALL applicable pattern rules
- **Verify requirements:** Confirm this file meets the original feature requirements
- **Document the feature:** Create/update documentation following project documentation patterns
- **ONLY IF ALL CHECKS PASS:** Mark this file as truly complete

## CRITICAL: ONE FILE AT A TIME ONLY
- **NEVER create multiple files in one response**
- **NEVER say "Now let me create the next file"**
- **COMPLETE ALL 7 STEPS for the current file BEFORE even mentioning another file**
- **MUST run lint and type check on THIS FILE before moving on**
- **MUST run any tests written for THIS FILE before moving on**
- Each file must go through: pattern check → analysis → implement → verify → types → test → final validation & documentation
- Only after all 7 steps pass completely should you consider the next file

---

## Backend Patterns - Production Quiz App

### Aspect 1: API Endpoint Structure and Naming

1. Blueprint-based route organization with url_prefix: This project uses Flask blueprints for organizing routes, not direct @app.route decorators. Each feature area has its own blueprint file in `app/routes/` (e.g., `auth.py` defines `auth_bp = Blueprint("auth", __name__)`). Blueprints are registered in `app/__init__.py:97` with URL prefixes like `app.register_blueprint(auth_bp, url_prefix="/auth")`, making all auth routes accessible at /auth/* paths.

2. Verb-noun URL naming pattern: Route URLs use lowercase verb-noun combinations with hyphens, never camelCase or underscores. Examples from `app/routes/auth.py`: `/register`, `/login`, `/logout`, `/verify/<token>`, `/forgot-password`, `/reset-password/<token>`, `/change-password`. The URL path is the action verb in kebab-case, not RESTful resource naming like `/users` or `/sessions`.

3. Template-based HTML response pattern with flash messages: All route functions return `render_template()` calls with Jinja2 templates, never JSON responses. User feedback is provided via `flash(message, category)` before redirects or renders. Example from `app/routes/auth.py:48`: `flash("Registration successful! Please check your email to verify your account.", "success")` followed by `return redirect(url_for("auth.login"))`. No routes return JSON dictionaries or API-style responses.

4. Form-Service-Template integration pattern: Route functions follow a consistent pattern: (1) instantiate WTForm, (2) check `form.validate_on_submit()`, (3) call static service method with form data, (4) handle tuple return `(result, error)`, (5) flash message, (6) redirect or render. Example from `app/routes/auth.py:37-51`: `user, error = AuthService.register_user(...)` → `if error: flash(error, "danger")` → `else: flash(..., "success"); return redirect(...)`. Services handle all business logic, routes only orchestrate.

5. Token-in-URL-path pattern for email verification and password reset: Token-based routes use URL path parameters `<token>`, not query strings. Example from `app/routes/auth.py:103`: `@auth_bp.route("/verify/<token>")` accessed as `/auth/verify/abc123token`, not `/auth/verify?token=abc123`. The token variable is passed directly to the function parameter: `def verify_email(token):`. Same pattern for password reset at `app/routes/auth.py:141`: `/reset-password/<token>`.

### Aspect 2: File Organization and Folder Structure

6. One model/service/form per file with snake_case naming: Database models are split into separate files in `app/models/`, one per entity: `user.py`, `quiz.py`, `question.py`, `attempt.py`, `user_answer.py`. Services follow the same pattern in `app/services/`: `auth_service.py`. Forms are grouped by feature area in `app/forms/`: `auth_forms.py` contains all authentication forms (RegistrationForm, LoginForm, etc.). Never use generic filenames like `models.py` or `services.py` at the top level.

7. Explicit __init__.py imports with __all__ for package exports: Every package directory has an `__init__.py` that explicitly imports all public classes/functions and defines `__all__` list. Example from `app/models/__init__.py:7-19`: imports all models (`from app.models.user import User`) then defines `__all__ = ["User", "Quiz", "Question", "Attempt", "UserAnswer"]`. This enables clean imports elsewhere: `from app.models import User` instead of `from app.models.user import User`. Never leave __init__.py empty.

8. Feature-based grouping not layer-based: Files are grouped by feature domain, not technical layer. For example, `app/forms/auth_forms.py` contains all authentication-related forms (registration, login, password reset), not separated into separate files per form type. Routes are organized by feature area (`auth.py`, `dashboard.py`), not by HTTP method or technical pattern. This feature-based organization makes related code easy to find.

9. Application factory pattern with separate entry point: The Flask app is created using an application factory function in `app/__init__.py:23`: `def create_app(config_name=None): return app`. The entry point is a separate `run.py:12` at project root that calls `app = create_app()` and runs the dev server. Never create the app instance directly in __init__.py or use `if __name__ == '__main__'` in __init__.py. This separation enables testing with different configs.

10. Test structure mirrors app structure with test_ prefix: Tests are organized in `tests/` with three subdirectories: `unit/`, `integration/`, `e2e/`. Test files are named with `test_` prefix matching the module under test: `tests/unit/test_models.py` tests `app/models/`, `tests/unit/test_services.py` tests `app/services/`, `tests/integration/test_auth_flow.py` tests authentication routes in `app/routes/auth.py`. This mirroring makes it easy to find tests for any module.

### Aspect 3: Database Queries and Transactions

11. Try-except-commit-rollback pattern for all database writes: All service methods that modify database data wrap operations in try-except blocks. On success, call `db.session.commit()`. On any exception, call `db.session.rollback()` and return error tuple. Example from `app/services/auth_service.py:31-62`: `try: ... db.session.add(user); db.session.commit(); return user, None; except Exception as e: db.session.rollback(); return None, "Registration failed."`. Never commit without try-except protection.

12. Model methods contain business logic, services manage transactions: Database models define business logic methods like `set_password()`, `check_password()`, `generate_verification_token()`, `record_failed_login()` in `app/models/user.py:74-194`. Services call these model methods, then manage the database session (commit/rollback). Example from `app/services/auth_service.py:46-52`: `user.set_password(password); user.generate_verification_token(); db.session.add(user); db.session.commit()`. Model methods modify object state, services persist changes.

13. Query.filter_by() for simple equality, Query.filter() for complex conditions: Simple lookups by single field use `Model.query.filter_by(field=value).first()`. Example from `app/services/auth_service.py:33`: `User.query.filter_by(username=username).first()`. Complex queries with OR/AND conditions use `Model.query.filter()` with SQLAlchemy expressions like `(User.username == x) | (User.email == x)`. Never use filter_by() for anything other than simple field equality.

14. Direct model instantiation followed by explicit db.session.add(): New database objects are created with direct instantiation `obj = Model(field=value)`, then explicitly added to session with `db.session.add(obj)`, then committed. Example from `app/services/auth_service.py:41-52`: `user = User(username=username, email=email); db.session.add(user); db.session.commit()`. Never rely on implicit session tracking or skip the add() call for new objects.

15. No intermediate db.session.flush() - only commit() or rollback(): Database operations use only `db.session.commit()` for success or `db.session.rollback()` for errors. Never use `db.session.flush()` for intermediate persistence. The pattern from `app/services/auth_service.py:222` is: modify objects → `db.session.commit()` (or rollback on exception). Flush is never needed because transactions are short and complete atomically.

### Aspect 4: Authentication and Authorization

16. Flask-Login with @login_required decorator for protected routes: Protected routes use `@login_required` decorator from `flask_login` module. Import pattern from `app/routes/auth.py:8`: `from flask_login import current_user, login_required, login_user, logout_user`. Decorator must come after route decorator, example from `app/routes/auth.py:93-95`: `@auth_bp.route("/logout")` then `@login_required` then `def logout():`. This automatically redirects unauthenticated users to login page.

17. User loader function defined in app factory initialize_extensions(): The Flask-Login user loader is defined inside `initialize_extensions()` in `app/__init__.py:84-87` as a nested function with decorator: `@login_manager.user_loader def load_user(user_id): return User.query.get(int(user_id))`. It converts user_id string to int and queries User model. This loader is called automatically by Flask-Login to load the user object from session user_id.

18. current_user proxy object for accessing logged-in user state: Routes access the current authenticated user via `current_user` imported from `flask_login`, never by querying `User.query.get(session['user_id'])`. Example from `app/routes/auth.py:97`: `username = current_user.username`. Check authentication status with `current_user.is_authenticated` (example from `app/routes/auth.py:30`), call model methods with `current_user.get_stats()` (example from `app/routes/auth.py:204`). current_user is a thread-local proxy that Flask-Login manages.

19. Redirect authenticated users away from login/register routes: Login and registration routes check `if current_user.is_authenticated:` at the start and redirect to dashboard to prevent duplicate logins. Example from `app/routes/auth.py:30-31`: `if current_user.is_authenticated: return redirect(url_for("dashboard.index"))`. Same pattern in login at line 61 and password reset routes at lines 121 and 145. This prevents authenticated users from accessing authentication pages.

20. Multi-layered authentication checks with account lockout: The `authenticate_user()` service method in `app/services/auth_service.py:78-117` performs ordered security checks: (1) user exists via query, (2) `user.is_account_locked()` returns False (unlocked after 15 min or <5 failed attempts), (3) `user.is_active` is True (account not deactivated), (4) `user.check_password(password)` returns True. Failed password checks call `user.record_failed_login()` then commit (line 102-103), which auto-locks account after 5 attempts. Successful login calls `user.reset_failed_logins()` and `user.update_last_active()` (lines 107-108).

### Aspect 5: Request Validation

21. Flask-WTF forms with declarative field validators: All forms inherit from `FlaskForm` (Flask-WTF, never raw WTForms) and define validation declaratively in field constructors. Import pattern from `app/forms/auth_forms.py:7-9`: `from flask_wtf import FlaskForm; from wtforms import StringField, PasswordField; from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo`. Example field from line 17: `username = StringField("Username", validators=[DataRequired(message="..."), Length(min=3, max=80, message="..."), Regexp("^[A-Za-z0-9_]+$", message="...")])`. CSRF protection is automatic with FlaskForm.

22. Custom validate_<fieldname> methods for database and complex checks: Forms define custom validation methods named `validate_<fieldname>(self, fieldname)` that are called automatically during validation. These methods query the database or perform complex checks, then raise `ValidationError("message")` on failure. Example from `app/forms/auth_forms.py:56-60`: `def validate_username(self, username): user = User.query.filter_by(username=username.data).first(); if user: raise ValidationError("Username already taken.")`. Method name must match field name exactly.

23. form.validate_on_submit() checks HTTP method, CSRF, and all validators: Routes check `if form.validate_on_submit():` which returns True only if: (1) request method is POST or PUT, (2) CSRF token is valid (automatic with FlaskForm), (3) all field-level validators pass, (4) all custom `validate_*` methods pass. Example from `app/routes/auth.py:35`. Never manually check request.method or CSRF - validate_on_submit() handles it. This single check replaces 3-4 separate validations.

24. Explicit user-facing messages in all validators: Every validator includes explicit `message=` parameter with clear, user-friendly error text that will be displayed to users. Example from `app/forms/auth_forms.py:20-25`: `DataRequired(message="Username is required")`, `Length(min=3, max=80, message="Username must be between 3 and 80 characters")`, `Regexp("^[A-Za-z0-9_]+$", message="Username must contain only letters, numbers, and underscores")`. Never rely on default validator messages - always provide custom messages.

25. Password strength validation in custom validate_password method: Password complexity requirements (uppercase, lowercase, digit) are enforced in a custom `validate_password(self, password)` method that checks `password.data` string with Python any() + generator expressions. Example from `app/forms/auth_forms.py:70-84`: `if not any(c.isupper() for c in pwd): raise ValidationError("Password must contain at least one uppercase letter")`. Same checks in RegistrationForm line 70 and ResetPasswordForm line 148. This method runs automatically when form is validated, no separate call needed.

### Aspect 6: Error Handling and Exceptions

26. Global error handlers registered in app factory for common HTTP codes: Error handlers for HTTP status codes (400, 401, 403, 404, 429, 500, 503) are registered in `register_error_handlers(app)` function defined in `app/__init__.py:192-239`. This function is called from `create_app()` during app initialization. Each handler uses `@app.errorhandler(status_code)` decorator and returns tuple of `(response, status_code)`. Example from line 195: `@app.errorhandler(400) def bad_request(error): return render_template_or_json("errors/400.html", error=error), 400`. Never register error handlers in routes.

27. Blueprint-specific error handlers for localized error behavior: Blueprints define their own error handlers for specific status codes using `@blueprint_name.errorhandler(status_code)` that override global handlers within that blueprint's routes. Example from `app/routes/auth.py:238-242`: `@auth_bp.errorhandler(429) def ratelimit_handler(e): flash("Too many requests."); return render_template("errors/429.html"), 429`. Blueprint handlers can flash messages and redirect, while global handlers render generic error pages. This allows auth blueprint's 404 to redirect to login (line 245), while other 404s show error page.

28. Tuple return pattern in services, never raise exceptions to callers: Service methods never raise exceptions to calling code. All service methods use try-except blocks internally and return tuples: `(result, error_message)` or `(success, message)`. Example pattern from `app/services/auth_service.py:31-62`: `try: ... return user, None; except Exception as e: db.session.rollback(); return None, "Error message"`. Callers check the tuple (if error: handle error) rather than catching exceptions. This makes error handling explicit and forces callers to handle failures.

29. render_template_or_json helper for graceful error page fallback: The `render_template_or_json(template_name, error, **kwargs)` helper in `app/__init__.py:242-249` attempts to render an error template, and if template doesn't exist (TemplateNotFound), falls back to JSON response with error details. Used in all error handlers: `return render_template_or_json("errors/404.html", error=error), 404`. This prevents secondary errors (500s) during error handling if error templates haven't been created yet, allowing app to work gracefully during development.

30. Selective logging: only 500 errors logged, no logging for client errors: Only internal server errors (500) are logged with `app.logger.error(f"Internal Server Error: {error}")` as seen in `app/__init__.py:231`. Client errors (400, 401, 403, 404) and rate limit errors (429) are NOT logged to avoid filling logs with malicious requests, bot traffic, or user mistakes. Service methods log significant events (successful login, registration) at INFO level, errors at ERROR level, but routes never log. This keeps logs focused on actionable server issues.

### Aspect 7: Service and Controller Organization

31. Service classes with all @staticmethod, no instance state: Service classes are purely organizational containers with all methods decorated with `@staticmethod`, never instance methods. Example from `app/services/auth_service.py:13-17`: `class AuthService:` followed by `@staticmethod def register_user(username, email, password):`. Services have no `__init__` method, no `self` parameter (except in decorator), no instance variables. This makes services stateless and allows direct calls like `AuthService.register_user()` without instantiation.

32. Routes are thin controllers that delegate to services: Route functions contain minimal logic - they only handle HTTP concerns (form validation, flash messages, redirects) and delegate all business logic to service methods. Example from `app/routes/auth.py:35-51`: route instantiates form, calls `form.validate_on_submit()`, calls `AuthService.register_user()`, handles the tuple return with flash/redirect. Routes never directly query models, never contain business logic like password hashing or validation. This separation makes business logic testable independently from HTTP layer.

33. One service class per feature domain matching route blueprint: Service organization mirrors route blueprint organization - each feature area has one service class. Example: `auth_service.py` contains `AuthService` class serving all methods needed by `auth_bp` blueprint in `app/routes/auth.py`. Service file names use `_service.py` suffix, class names use `Service` suffix (AuthService, not Auth). If a quiz_bp blueprint existed, there would be `quiz_service.py` with `QuizService` class. Never create generic services like `DatabaseService` or `HelperService`.

34. Service methods call model methods for domain logic, never implement it: Services orchestrate operations by calling model methods like `user.set_password()`, `user.generate_verification_token()`, `user.check_password()`, never implementing the logic directly. Example from `app/services/auth_service.py:46-49`: `user.set_password(password); user.generate_verification_token()`. The password hashing algorithm is in `User.set_password()` at `app/models/user.py:82`, not in the service. Services handle transaction boundaries and orchestration, models contain domain logic and state mutation.

35. Placeholder methods with TODO comments and logging for unimplemented integrations: External integrations that aren't implemented yet (email sending, SMS, etc.) have service methods that log what would happen and return success, marked with `# TODO:` comments. Example from `app/services/auth_service.py:314-341`: `send_verification_email()` method logs verification URL with `current_app.logger.info()` and returns `True`, with TODO comment and example integration code in comments. This allows features to work end-to-end during development before external services are integrated.

### Aspect 8: Database Migrations

36. Alembic migrations with Flask-Migrate, autogenerated from models: This project uses Alembic via Flask-Migrate for database migrations. Migrations are autogenerated by comparing models to database schema with `flask db migrate -m "message"` command, which creates versioned migration files in `migrations/versions/`. Example: `d0a72a14ad60_initial_production_schema_with_enhanced_.py`. Migrations are NOT written manually - model changes drive migration generation. The `migrations/env.py:18-24` integrates Alembic with Flask app context via `current_app.extensions['migrate']`.

37. Inline constraints in models with __table_args__, not in migrations: Database constraints (CheckConstraint, UniqueConstraint) are defined in model `__table_args__` tuples, which Alembic detects and includes in autogenerated migrations. Example from `app/models/user.py:60-66`: `__table_args__ = (db.Index('idx_user_username', 'username'), db.CheckConstraint('failed_login_attempts >= 0'), )`. The migration file at `migrations/versions/d0a72a14ad60...py:52` shows autogenerated `sa.CheckConstraint('failed_login_attempts >= 0')`. Never manually edit migration files to add constraints - add to model and regenerate.

38. Batch mode for index creation using with op.batch_alter_table(): Index creation in migrations uses batch mode via `with op.batch_alter_table('table_name', schema=None) as batch_op:` followed by `batch_op.create_index()` calls. Example from migration line 34: `with op.batch_alter_table('quizzes', schema=None) as batch_op: batch_op.create_index('idx_quiz_category', ['category'], unique=False)`. This is required for SQLite compatibility (SQLite doesn't support ALTER TABLE for many operations). Batch mode works for all databases, so it's used consistently.

39. Complete upgrade() and downgrade() functions for rollback capability: Every migration has both `upgrade()` and `downgrade()` functions. upgrade() applies changes, downgrade() reverses them in opposite order. Example from migration lines 133-168: downgrade drops tables in reverse order (user_answers → questions → attempts → users → quizzes) and drops indexes before tables. This ensures `flask db downgrade` can always roll back changes. Downgrade is autogenerated by Alembic, not manually written.

40. Migration metadata includes revision chain and descriptive docstring: Migration files start with docstring containing description, revision ID, parent revision, and creation timestamp. Example from migration lines 1-16: `"""Initial production schema with enhanced User model and constraints\n\nRevision ID: d0a72a14ad60\nRevises:\nCreate Date: 2025-12-19 13:58:59"""` followed by module-level variables `revision`, `down_revision`, `branch_labels`, `depends_on`. The `down_revision = None` indicates first migration. Subsequent migrations would have `down_revision = 'parent_revision_id'`, forming a chain.

### Aspect 9: Async Operation Patterns

41. Synchronous execution only, no async/await or background tasks: This project uses synchronous Python code exclusively - no `async def`, `await`, `asyncio`, or background task queues like Celery. All route handlers, service methods, and model methods execute synchronously in the request-response cycle. Grep for `async def|await |asyncio\.|celery|@task` returns no matches in the codebase. Email sending (placeholder) and other potentially slow operations execute inline, not in background workers.

42. No async framework or ASGI server: The application runs on Gunicorn with sync workers (WSGI), not ASGI servers like Uvicorn or Hypercorn. No use of async frameworks like FastAPI or async Flask views. Configuration in `Dockerfile` uses `gunicorn` with `--workers` flag (sync worker model), not `--worker-class uvicorn.workers.UvicornWorker`. This is a traditional synchronous Flask application.

43. Long-running operations would block request thread: Operations like email sending (`app/services/auth_service.py:314-341`) that could take seconds are implemented as synchronous calls. In current placeholder implementation, they only log and return immediately, but if implemented with real SMTP calls, they would block the request thread. No queue system exists to offload these operations. This is acceptable for low-traffic applications but would need Celery/RQ for high-traffic production use.

44. Database queries execute synchronously with no connection pooling config: All database queries via SQLAlchemy execute synchronously in the request thread. No explicit connection pool configuration in `app/config.py` - relies on SQLAlchemy defaults. No use of async SQLAlchemy features. Query patterns like `User.query.filter_by(username=username).first()` block until results return. No `.options(defer())` or streaming queries for large datasets.

45. Rate limiting uses Redis or in-memory storage, not queue-based: Flask-Limiter configuration at `app/config.py:38` uses `RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL") or "memory://"` for synchronous rate limit checking. No message queue for rate limit enforcement. Requests are checked against Redis/memory counters synchronously before route execution. No pub/sub or background processing for rate limit violations.

### Aspect 10: Logging and Monitoring

46. RotatingFileHandler with size and backup limits, not production-only: Logging is configured in `configure_logging()` function at `app/__init__.py:159-189` using `logging.handlers.RotatingFileHandler`. Configuration: `maxBytes=10485760` (10MB per file), `backupCount=10` (10 backup files), creating at most ~100MB logs. Handler is added only when `not app.debug and not app.testing` (line 161), so development and test environments skip file logging. Log file path from `app.config.get("LOG_FILE")` with automatic directory creation (lines 169-176).

47. current_app.logger for service-level logging, app.logger for app-level: Service methods use `current_app.logger` imported from Flask to access the application logger within request context. Example from `app/services/auth_service.py:55`: `current_app.logger.info(f"New user registered: {username}")`. App-level code uses `app.logger` directly, as seen in `app/__init__.py:144`: `app.logger.error(f"Health check database error: {e}")`. Never use Python's `logging.getLogger(__name__)` pattern - always use Flask's logger.

48. Structured log format with timestamp, level, module, message: Log messages use format string `"[%(asctime)s] %(levelname)s in %(module)s: %(message)s"` configured at `app/__init__.py:184`. This produces logs like `[2025-12-19 10:30:45] INFO in auth_service: New user registered: john`. The module name helps trace which file generated the log. Message always uses f-string with context variables, never bare strings. Example: `f"User logged in: {user.username}"` not `"User logged in"`.

49. Health check endpoint with database and cache connectivity tests: The `/health` route at `app/__init__.py:118-156` returns JSON with connectivity status for database and cache. Database check executes `SELECT 1` query (line 139), cache check calls `cache.cache.get("health_check")` (line 149). Returns 200 if healthy, 503 if unhealthy. Health status dict includes `status`, `timestamp`, `service`, `version`, `database`, `cache` fields. Load balancers and monitoring tools use this endpoint to detect service degradation.

50. Optional Sentry integration with Flask integration and sampling: Sentry error tracking is initialized in `initialize_sentry()` at `app/__init__.py:272-293` only if `SENTRY_DSN` env var is set and not testing. Configuration uses `FlaskIntegration()` to capture Flask request context, `traces_sample_rate=0.1` (10% of transactions), `profiles_sample_rate=0.1` (10% profiling), and `environment` from FLASK_ENV. If Sentry SDK not installed, logs warning but continues. Sentry captures unhandled exceptions automatically, no explicit `sentry_sdk.capture_exception()` calls needed.

### Aspect 11: Testing Patterns

51. Pytest with session-scoped app and function-scoped client fixtures: Tests use pytest fixtures defined in `tests/conftest.py`. The `app` fixture (line 17) has `scope="session"` and creates app once per test session with `create_app("testing")`, establishing app context with `with app.app_context():`. The `client` fixture (line 43) has `scope="function"` and creates new test client per test with `app.test_client()`. Tests receive fixtures as function parameters: `def test_something(app, client):`. Never create app or client manually in test functions.

52. Transaction-based test isolation with db_session fixture and rollback: The `db_session` fixture in `tests/conftest.py:63-80` provides transaction rollback isolation. Pattern: begin transaction with `connection.begin()` (line 74), bind session to connection, yield session to test, then rollback transaction (line 85). Each test gets clean database state without recreating tables. Tests use `with app.app_context():` wrapper and call factories which auto-commit, then rollback discards all changes. Never call `db.drop_all()` between tests.

53. Factory Boy factories with inheritance and PostGenerationMethodCall: Test data is created with Factory Boy factories in `tests/factories.py`. All factories inherit from `BaseFactory` which sets `sqlalchemy_session = db.session` and `sqlalchemy_session_persistence = "commit"` (lines 17-27). Example from `UserFactory` (lines 30-55): `username = factory.Sequence(lambda n: f"user{n}")` for unique values, `email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")` for derived values, `password_hash = factory.PostGenerationMethodCall("set_password", "TestPass123")` to call model methods after creation. Factory subclasses override fields: `AdminUserFactory(UserFactory): is_admin = True`.

54. Pytest markers for test categorization: Tests use `@pytest.mark.*` decorators for categorization. Examples from `tests/unit/test_models.py:24-26`: `@pytest.mark.unit` and `@pytest.mark.models` before test class. Integration tests use `@pytest.mark.integration` and `@pytest.mark.auth` (from `tests/integration/test_auth_flow.py:16-17`). This enables running subsets with `pytest -m unit` or `pytest -m "integration and auth"`. Test classes group related tests: `class TestUserModel:` groups all User model tests.

55. Integration tests use client.post() with follow_redirects and status code ranges: Integration tests post form data with `client.post("/route", data={...}, follow_redirects=False)` pattern. Example from `tests/integration/test_auth_flow.py:31-44`: posts registration data, then asserts `response.status_code in [200, 302, 400]` because CSRF validation might fail in tests without real tokens. Always specify `follow_redirects=False` to test redirect behavior explicitly. Never assume single status code - account for CSRF/validation failures with status code ranges or lists.

### Aspect 12: Permissions and Security Patterns

56. Rate limiting with @limiter.limit decorator per route, not global: Route-specific rate limits use `@limiter.limit("count per period")` decorator above route definitions. Examples from `app/routes/auth.py`: `@limiter.limit("3 per hour")` for registration (line 26), `@limiter.limit("5 per 15 minutes")` for login (line 57), `@limiter.limit("3 per hour")` for password reset (line 117). Comments specify the limit intent. Limits apply per IP address (default key_func). No global rate limit - each sensitive endpoint has specific limits. Testing config disables rate limiting with `RATELIMIT_ENABLED = False` (app/config.py:117).

57. Boolean permission flags on User model, no role-based access control: User permissions use simple boolean flags: `is_active` (account enabled/disabled) and `is_admin` (admin privileges). Defined in `app/models/user.py:37-38`: `is_active = db.Column(db.Boolean, default=True, nullable=False); is_admin = db.Column(db.Boolean, default=False, nullable=False)`. Authentication checks `is_active` status in `app/services/auth_service.py:96`: `if not user.is_active: return None, "Account is deactivated."`. No role system (roles table, many-to-many), no permission objects - just two boolean columns.

58. Security headers configured in production config and applied via after_request: Security headers are defined in `ProductionConfig.SECURITY_HEADERS` dict in `app/config.py`, then applied to all responses via `@app.after_request` decorator in `configure_security_headers()` at `app/__init__.py:258-269`. Pattern: `for header, value in security_headers.items(): response.headers[header] = value`. Headers include X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, CSP, HSTS. No per-route header customization - same headers on all responses. Development config has no security headers or less strict ones.

59. CSRF protection automatic with Flask-WTF, disabled only in testing: CSRF tokens are automatically generated and validated by Flask-WTF when using FlaskForm. Configuration in `BaseConfig` at `app/config.py:34-35`: `WTF_CSRF_ENABLED = True; WTF_CSRF_TIME_LIMIT = None`. Testing config disables CSRF at line 114: `WTF_CSRF_ENABLED = False`. Forms automatically include CSRF token field, routes check it via `form.validate_on_submit()`. No manual `csrf.protect()` calls or custom CSRF handling - entirely automatic through WTF forms.

60. No permission decorators or route-level authorization beyond login_required: Routes use only `@login_required` decorator for authentication, no custom permission decorators like `@admin_required` or `@permission_required('edit_quiz')`. If admin-only routes existed, they would check `current_user.is_admin` inside the route function body, not via decorator. Example hypothetical pattern: `if not current_user.is_admin: flash("Unauthorized"); return redirect(...)`. No declarative permission system - permission checks are imperative if/else statements when needed.

### Aspect 13: Caching Patterns

61. Flask-Caching initialized but not actively used, infrastructure ready: Caching is configured via `cache = Cache()` in `app/extensions.py:39` and initialized with `cache.init_app(app)` in `app/__init__.py:81`, but no routes or services use `@cache.cached` decorators or `cache.get()`/`cache.set()` calls. The infrastructure is ready (health check tests it at line 149), but caching is not implemented yet. Grep for `@cache\.|cache\.get|cache\.set` returns only health check usage, no actual caching logic.

62. Environment-dependent cache backend: SimpleCache for dev, RedisCache for production: Cache backend varies by environment via `CACHE_TYPE` config. Development uses `CACHE_TYPE = "SimpleCache"` (in-memory, single-process) at `app/config.py:99`. Production uses `CACHE_TYPE = "RedisCache"` with `CACHE_REDIS_URL = REDIS_URL` at lines 171-172. Testing also uses SimpleCache (line 120). Staging config would use RedisCache. Cache backend switches automatically based on environment - no code changes needed.

63. Default cache timeout of 300 seconds in base config: Cache timeout is set globally in `BaseConfig` at `app/config.py:44`: `CACHE_DEFAULT_TIMEOUT = 300` (5 minutes). This applies to all cached items unless overridden with `timeout=` parameter in `@cache.cached()` decorator or `cache.set()` call. No per-route or per-function timeout configuration exists yet since caching isn't actively used. When caching is implemented, 300 seconds is the fallback for any cache operations without explicit timeout.

64. Cache health check in health endpoint tests connectivity: The `/health` endpoint includes cache connectivity test at `app/__init__.py:146-153`: `if cache.cache: cache.cache.get("health_check"); health_status["cache"] = "connected"`. This tests that Redis (in production) or SimpleCache is accessible. If cache fails, logs warning but marks cache as "disconnected" without failing overall health check. Health status remains "healthy" even if cache is down - cache is not critical for application operation.

65. No cache warming, invalidation, or tagging patterns: No code exists for cache warming (pre-populating cache on startup), cache invalidation (clearing specific keys on updates), or cache tagging (grouping related cache keys). When caching is implemented, it will require manual `cache.delete(key)` or `cache.clear()` calls for invalidation. No decorator-based invalidation like `@cache.invalidate()` or tag-based clearing. Cache operations will be explicit, not declarative.

### Aspect 14: Background Jobs and Queues

66. No background job system, all operations synchronous: No background job queue system like Celery, RQ, or Huey is installed or configured. All operations execute synchronously in the request-response cycle. Grep for `celery|@task|rq\.|huey` returns no matches in app code. Email sending, report generation, and other potentially long-running operations would block the request thread if implemented with real external services. This architecture is suitable for low-traffic applications but limits scalability.

67. No task queue infrastructure or worker processes: No Redis queue, no worker process management, no task retry logic, no task status tracking. The application has only web workers (Gunicorn), no separate background workers. Docker Compose and deployment configs define only the web service, no worker service. If background jobs are needed in the future, would require adding Celery/RQ, creating worker Dockerfile, and deploying separate worker instances.

68. Placeholder email methods execute inline without queuing: Email operations in `app/services/auth_service.py:314-363` are synchronous methods that currently only log (placeholders). When implemented with real SMTP (Flask-Mail or similar), these would execute inline, blocking the request. Example: registration at `app/routes/auth.py:45` calls `AuthService.send_verification_email(user)` synchronously before responding. No `send_email.delay()` or `queue_email()` pattern exists.

69. No scheduled tasks or periodic jobs: No cron-like scheduled tasks exist for periodic operations like cleanup, report generation, or data synchronization. No Celery Beat, no APScheduler, no system cron jobs defined. If periodic tasks are needed, would require either system cron calling Flask CLI commands, or adding Celery Beat with periodic task definitions. No infrastructure exists for recurring background work.

70. No task result storage or callback patterns: No mechanism exists to track background task status, retrieve results, or execute callbacks on completion. No Result backend (Redis, database), no task IDs, no polling endpoints like `/tasks/<task_id>/status`. All operations are fire-and-forget or immediate return. If background tasks are added, would need to implement result tracking from scratch or use Celery's result backend.

### Aspect 15: File Upload and Storage

71. No file upload functionality, forms are text-only: No file upload fields exist in any forms. Forms in `app/forms/` use only StringField, PasswordField, BooleanField, SubmitField - no FileField or file validators. Grep for `upload|FileField|request\.files` returns no matches in app code. Routes never access `request.files`. The application has no user-uploaded content (avatars, documents, images) - purely text-based data (username, email, quiz answers).

72. Static files served from app/static/, no user upload directory: The `app/static/` directory contains only application assets (CSS, JS, images) deployed with the application. No `uploads/` or `media/` directory exists for user-uploaded files. Flask serves static files from this directory in development with `url_for('static', filename='...')`. In production, Nginx serves static files directly (configured in `deployment/nginx/nginx.conf`). No separate file storage service (S3, Cloudinary) is configured.

73. No file validation, processing, or storage utilities: No utility functions exist for file upload handling - no file type validation, size limits, sanitization, thumbnail generation, or virus scanning. No storage abstraction layer (local filesystem vs S3). If file uploads are added, would need to implement security checks (file extension whitelist, magic number validation, size limits), filename sanitization (removing special chars, generating unique names), and storage logic from scratch.

74. No CDN or external storage integration: No configuration exists for CDN (CloudFront, Cloudflare) or cloud storage (AWS S3, Azure Blob, Google Cloud Storage). All assets are served directly from the Flask application or Nginx static file serving. The `STATIC_FOLDER` and `STATIC_URL_PATH` use Flask defaults (app/static/). No boto3, google-cloud-storage, or azure-storage-blob dependencies in requirements files.

75. Template references to static files use url_for('static'): Templates reference static assets with `url_for('static', filename='path/to/file')` pattern, not hardcoded paths. This is Flask's standard static file handling. Example would be `<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">` in base.html. No custom static file serving logic exists - relies entirely on Flask/Nginx built-in static file serving.

### Aspect 16: Email and Notification Patterns

76. Email configuration in BaseConfig but no Flask-Mail initialization: Email settings are defined in `app/config.py:52-58`: `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER` from environment variables. However, Flask-Mail is NOT initialized in `app/extensions.py` - no `mail = Mail()` or `mail.init_app(app)`. The configuration exists but the email extension is not installed or configured. Requirements files don't include Flask-Mail or similar email libraries.

77. Placeholder send_email methods that only log, marked with TODO: Email sending methods in `app/services/auth_service.py` are placeholders. `send_verification_email()` at line 314 and `send_password_reset_email()` at line 344 only log URLs with `current_app.logger.info()` and return `True`. Both have `# TODO: Implement actual email sending` comments and example Flask-Mail code in comments (lines 333-339, 361-362). No actual SMTP connection, no email templates, no email queueing. This allows development and testing without email infrastructure.

78. Email methods called synchronously in request flow, never queued: Routes call email methods synchronously after database operations. Example from `app/routes/auth.py:45`: after successful registration, calls `AuthService.send_verification_email(user)` before flash and redirect. Password reset at line 133 is similar: `AuthService.send_password_reset_email(user)`. No background job queue, no `send_email.delay()` pattern. When real email sending is implemented, it will block the request thread unless moved to background queue.

79. No email templates, transactional email service, or email tracking: No HTML/text email templates exist (no `templates/emails/` directory). No integration with transactional email services like SendGrid, Postmark, or AWS SES. No email tracking (opens, clicks, bounces, delivery status). No email validation beyond WTForms Email validator. If real email is implemented, would need to create templates, choose service (SMTP vs API-based), and potentially add tracking if needed for production monitoring.

80. Security: Always show success message even if email doesn't exist: Password reset flow at `app/routes/auth.py:126-136` always shows success message regardless of whether email exists in database: "If your email is registered, you will receive password reset instructions." Line 132 checks `if user:` but doesn't reveal non-existence. This prevents email enumeration attacks. Comment at `app/forms/auth_forms.py:122` explains this security pattern. Same principle should apply to all email-based operations.

### Aspect 17: Rate Limiting and Throttling

81. Flask-Limiter with default limits and per-route overrides: Rate limiting is initialized in `app/extensions.py:32-36` with `Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"], storage_uri="memory://")`. Default limits apply to all routes unless overridden. Per-route limits use `@limiter.limit("N per period")` decorator. Example: registration has stricter limit `@limiter.limit("3 per hour")` overriding the defaults. The storage_uri is updated from config during init_app() to use Redis in production.

82. get_remote_address as key_func, limits enforced per IP: Rate limits are tracked per client IP address using `key_func=get_remote_address` from `flask_limiter.util`. This means 5 requests from IP 1.2.3.4 and 5 from IP 5.6.7.8 count separately. No user-based rate limiting (would need custom key_func returning user_id). Behind reverse proxy, ensure X-Forwarded-For header is trusted so get_remote_address returns real client IP, not proxy IP. No rate limit bypass for authenticated users or admins.

83. RATELIMIT_HEADERS_ENABLED shows remaining limits in response headers: Configuration `RATELIMIT_HEADERS_ENABLED = True` in `app/config.py:40` causes Flask-Limiter to add headers to responses: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`. Clients can check these headers to see how many requests remain before hitting the limit. Example: after 2 of 5 login attempts, headers show Limit: 5, Remaining: 3. No custom rate limit exceeded response format - uses default 429 error handler.

84. Rate limiting disabled in testing config: Testing configuration at `app/config.py:117` sets `RATELIMIT_ENABLED = False` to disable rate limiting during tests. This prevents tests from hitting rate limits when making multiple requests. Never disable rate limiting in production or staging - only testing and potentially local development if needed for debugging. Production has strict rate limits enabled by default.

85. Storage backend: memory:// for dev, Redis for production: Rate limit counters are stored in different backends per environment. Extensions default is `storage_uri="memory://"` (line 35) for simple in-memory storage. Production config overrides with `RATELIMIT_STORAGE_URL = REDIS_URL` at `app/config.py:173`, using Redis for distributed rate limiting across multiple web workers. Memory storage doesn't persist across restarts and doesn't work with multiple workers - only suitable for single-process development.

### Aspect 18: Configuration Management

86. Four-tier config class inheritance from BaseConfig: Configuration uses class inheritance in `app/config.py` with `BaseConfig` containing shared settings (lines 11-73), then four environment classes inherit: `DevelopmentConfig`, `TestingConfig`, `StagingConfig`, `ProductionConfig` (lines 75-209). Each overrides specific settings. Example: `DevelopmentConfig(BaseConfig):` inherits all base settings, then overrides `DEBUG = True`, `SQLALCHEMY_DATABASE_URI = SQLite`, `CACHE_TYPE = "SimpleCache"`. This avoids duplication - common settings defined once in BaseConfig.

87. get_config() function with FLASK_ENV fallback and config dict mapping: Configuration selection happens via `get_config(config_name)` function at `app/config.py:221-235`. It first uses passed `config_name`, then falls back to `FLASK_ENV` environment variable, then to "default" (which maps to DevelopmentConfig). The `config` dict at lines 212-218 maps string names to config classes: `{"development": DevelopmentConfig, "testing": TestingConfig, ...}`. Application factory calls this: `config_class = get_config(config_name); app.config.from_object(config_class)`.

88. Environment variables via os.environ.get() with or defaults: Configuration reads secrets and environment-specific values from environment variables using `os.environ.get("VAR_NAME")` with `or` operator for defaults. Example from `app/config.py:15`: `SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"`. Database URL at line 82: `SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///.../dev_quiz_app.db"`. Never hardcode secrets - always use environment variables with safe development defaults.

89. ProductionConfig.init_app() validates required environment variables: Production config has a `@classmethod init_app(cls, app)` method at lines 185-192 that raises `ValueError` if required environment variables are missing: DATABASE_URL, REDIS_URL, SECRET_KEY. This validation runs when production config is loaded, failing fast on startup if misconfigured. Development/testing configs don't validate because they have working defaults. Pattern: `if not cls.SQLALCHEMY_DATABASE_URI: raise ValueError("DATABASE_URL environment variable must be set in production")`.

90. Progressive security: permissive dev, strict production: Security settings progressively tighten across environments. Development has `DEBUG = True`, `SESSION_COOKIE_SECURE = False`, no HSTS (lines 78-94). Production has `DEBUG = False`, `SESSION_COOKIE_SECURE = True`, `SECURITY_HEADERS` with HSTS (lines 159-201). Testing disables CSRF and rate limiting for easier testing (lines 102-127). This allows rapid local development while enforcing security in production. Never set DEBUG = True in production.

### Aspect 19: Documentation Patterns

91. Comprehensive docs/ directory with multiple guides: Documentation is organized in `docs/` directory with separate files for different topics: `API.md` (API reference), `ARCHITECTURE.md` (system design), `DEPLOYMENT.md` (deployment instructions), `DEVELOPMENT.md` (developer workflow), `CONTRIBUTING.md` (contribution guidelines). Each guide is self-contained and linked from main README. No inline API docs generation (Sphinx, etc.) - documentation is manually written Markdown. This provides narrative documentation rather than just autogenerated API refs.

92. Triple-quoted module docstrings at file start: Every Python file starts with a triple-quoted docstring describing the module's purpose. Example from `app/services/auth_service.py:1-5`: `"""Authentication service with business logic.\n\nHandles user registration, login, password reset, email verification, etc."""`. Models, routes, forms all follow this pattern. Docstring appears before imports and describes what the module does, not implementation details. These serve as file-level comments for developers browsing code.

93. Function docstrings with Args and Returns sections: Service and model methods use docstrings with structured sections: description, Args (parameter names and descriptions), Returns (return value format). Example from `app/services/auth_service.py:17-30`: `"""Register a new user.\n\nArgs:\n    username: Desired username\n    email: User's email address\n    password: Plain text password (will be hashed)\n\nReturns:\n    tuple: (user, error_message)\n        user: User object if successful, None if failed\n        error_message: None if successful, error string if failed"""`. This documents the tuple return pattern explicitly.

94. TODO comments for unimplemented features with context: Placeholder functionality is marked with `# TODO:` comments that explain what needs to be implemented. Example from `app/services/auth_service.py:328`: `# TODO: Implement actual email sending` followed by commented example code (lines 333-339). Comments provide context about what the placeholder represents and what real implementation would look like. Never leave TODO comments without explanation of what needs to be done.

95. README.md with badges, structure overview, and quick start: Main README at project root includes badges (CI/CD, coverage, Python version, code style), features list, project structure tree, quick start commands, configuration guide, and links to detailed docs. Example sections: "Quick Start" (4 steps), "Configuration" (environment variables), "Documentation" (links to docs/ files). README serves as entry point - comprehensive enough to get started, detailed enough to understand architecture, with links to deep-dive docs.

### Aspect 20: Type Definitions and Language Patterns

96. No type hints, duck typing throughout: The codebase uses no Python type annotations. Functions and methods have no parameter types or return type hints like `def func(name: str) -> tuple[User, str]:`. Grep for `from typing|: str|: int|-> ` returns no matches in app code. The project relies on duck typing and docstring documentation rather than static type checking. No mypy configuration exists. This is common for Flask applications prioritizing rapid development over static type safety.

97. Python 3.9+ syntax with f-strings and modern features: Code uses modern Python features: f-strings for formatting (`f"User {user.username}"`), dictionary unpacking, type()\_\_name\_\_ for class names, pathlib in some places. Requirements specify `Python 3.9+` badge in README. No legacy Python 2.x compatibility code (no `from __future__ import`, no six library). F-strings used consistently over .format() or % formatting. Context managers (with statements) used for database transactions and file handling.

98. Werkzeug datastructures, Flask request/response, no custom types: The application uses Flask and Werkzeug built-in types: `request.form`, `request.args`, `session` (dict-like), `Response`, `redirect()`, `render_template()`. No custom type classes or dataclasses for request/response. Models return dictionaries or tuples, not custom response objects. Example: `User.get_stats()` returns dict, `AuthService.register_user()` returns tuple. No Pydantic models or attrs classes for data validation - WTForms handles that.

99. SQLAlchemy declarative models with db.Column types: Database models use SQLAlchemy's type system via `db.Column()` with type as first argument: `db.Column(db.String(80))`, `db.Column(db.Integer)`, `db.Column(db.Boolean)`, `db.Column(db.DateTime)`. These provide runtime type checking and database schema generation, not Python static type hints. Nullable specified with `nullable=False/True`, defaults with `default=value`. Models inherit from `db.Model` base class, not plain Python classes.

100. List comprehensions and generator expressions preferred: Code uses Pythonic patterns like list comprehensions and generator expressions. Example from password validation: `any(c.isupper() for c in pwd)`, `any(c.islower() for c in pwd)`, `any(c.isdigit() for c in pwd)` checking password strength. Factory Boy uses `factory.Sequence(lambda n: f"user{n}")` for unique values. Comprehensions preferred over map/filter for readability. Generator expressions used with any/all for short-circuit evaluation.

### Aspect 21: Build/Deployment Integration

101. Multi-stage Dockerfile with builder and runtime stages: Dockerfile uses multi-stage build pattern to minimize image size. Stage 1 (`FROM python:3.11-slim as builder`) creates virtual environment and installs dependencies. Stage 2 (`FROM python:3.11-slim`) copies only the venv and application code, not build tools. Example from Dockerfile lines 1-10: builder stage installs packages, runtime stage at line 12+ runs the application. Final image excludes pip, setuptools, and intermediate build files. This reduces attack surface and image size.

102. Non-root user in Docker container for security: Dockerfile creates and uses non-root user `appuser` for running the application. Pattern at lines 14-15: `RUN useradd --create-home --shell /bin/bash appuser` then `USER appuser` before CMD. Application files are chown'd to appuser with `COPY --chown=appuser:appuser`. Never run production containers as root - always create dedicated application user. This limits damage if container is compromised.

103. GitHub Actions CI pipeline with lint, test, and coverage jobs: CI pipeline in `.github/workflows/ci.yml` defines multiple jobs: `lint` (black, isort, flake8), `test` (pytest with coverage), potentially `build` (Docker image). Jobs run on `push` and `pull_request` events. Services like PostgreSQL and Redis are provided as Docker containers in the test job. Coverage results uploaded to codecov. Example job structure: `jobs: lint: runs-on: ubuntu-latest steps: [checkout, setup-python, run-linters]`. No deployment jobs - CI only validates code.

104. Split requirements files for different environments: Requirements are split into `requirements/base.txt`, `requirements/development.txt`, `requirements/testing.txt`, `requirements/production.txt`. Base contains core dependencies (Flask, SQLAlchemy), development adds dev tools (black, flake8, ipython), testing adds test tools (pytest, coverage, factory-boy), production adds production dependencies (gunicorn, sentry-sdk). Development/testing/production files all start with `-r base.txt` to include base dependencies. This prevents installing dev tools in production.

105. Gunicorn WSGI server configuration in CMD: Production container runs Gunicorn via Dockerfile CMD. Example command: `CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "sync", "run:app"]`. Configuration: 4 workers (sync worker class, not async), binds to all interfaces on port 8000, imports app from `run.py`. Worker count can be overridden via environment variable or docker-compose. Never use Flask development server (`python run.py`) in production - always use production WSGI server like Gunicorn or uWSGI.
