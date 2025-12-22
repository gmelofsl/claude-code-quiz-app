# CI/CD Pipeline Documentation

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the Production Quiz App.

## Overview

The CI/CD pipeline is implemented using **GitHub Actions** and runs automatically on:
- Push to `main` or `develop` branches
- Pull requests targeting `main` or `develop`

## Pipeline Jobs

### 1. Lint and Code Quality

**Purpose:** Ensure code quality and formatting standards

**Checks:**
- **Black**: Code formatting (line length: 100)
- **isort**: Import sorting
- **Flake8**: PEP 8 compliance and code complexity
- **Bandit**: Security vulnerabilities scan
- **Safety**: Dependency vulnerability check

**Run locally:**
```bash
# Format code
black app/ tests/ scripts/ --line-length 100
isort app/ tests/ scripts/ --profile black

# Check linting
flake8 app/ tests/ scripts/ --max-line-length=100 --max-complexity=10

# Security checks
bandit -r app/
safety check
```

### 2. Security Scan

**Purpose:** Identify security vulnerabilities

**Scans:**
- **Bandit**: Python security issues (SQL injection, hardcoded secrets, etc.)
- **Safety**: Known vulnerabilities in dependencies
- **Trivy**: Container and filesystem vulnerability scanner

**Results:** Uploaded as artifacts and to GitHub Security tab

### 3. Test Suite

**Purpose:** Run all tests with coverage reporting

**Matrix Strategy:** Tests run on Python 3.9, 3.10, 3.11, 3.12

**Services:**
- PostgreSQL 15 (database)
- Redis 7 (caching/sessions)

**Test Types:**
- Unit tests
- Integration tests
- End-to-end tests

**Coverage:**
- Minimum threshold: 70%
- Target: 80%+
- Reports uploaded to Codecov

**Run locally:**
```bash
# Run all tests with coverage
pytest tests/ -v --cov=app --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html
```

### 4. Integration Tests

**Purpose:** Test complete user workflows

**Dependencies:** Runs after lint and test jobs pass

**Services:**
- PostgreSQL (test database)
- Redis (test cache)

**Tests:**
- Authentication flows
- Quiz workflows
- API endpoints

### 5. Build Docker Image

**Purpose:** Build and push Docker image to registry

**Triggers:**
- Only on push to `main` branch
- After lint and test jobs pass

**Process:**
1. Build Docker image with BuildX
2. Tag with:
   - `latest`
   - Git SHA
   - Branch name
3. Push to Docker Hub (if credentials configured)
4. Scan with Trivy
5. Upload security results

**Manual build:**
```bash
docker build -f deployment/docker/Dockerfile -t quiz-app:latest .
```

### 6. Deploy to Production

**Purpose:** Automatically deploy to production server

**Triggers:**
- Push to `main` branch
- All previous jobs pass

**Process:**
1. SSH to production server
2. Pull latest code
3. Update Docker containers
4. Run database migrations
5. Restart services

**Environment:** `production` (requires approval)

## Required GitHub Secrets

Configure these in GitHub Settings → Secrets and Variables → Actions:

### Required for Basic CI/CD:
- `CODECOV_TOKEN`: Codecov upload token (optional but recommended)

### Required for Docker Build:
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password or access token

### Required for Deployment:
- `DEPLOY_HOST`: Production server hostname/IP
- `DEPLOY_USER`: SSH username
- `DEPLOY_SSH_KEY`: Private SSH key for authentication
- `DEPLOY_PORT`: SSH port (default: 22)

### Optional:
- `SLACK_WEBHOOK`: For Slack notifications
- `SENTRY_DSN`: For error tracking

## Branch Protection Rules

**Recommended settings for `main` branch:**

1. **Require pull request reviews**: 1 approval
2. **Require status checks to pass:**
   - lint
   - test (Python 3.11)
   - security
3. **Require branches to be up to date**
4. **Do not allow bypassing** (even for admins)
5. **Require signed commits** (optional)

## Pull Request Workflow

1. **Create feature branch** from `develop`
   ```bash
   git checkout -b feature/my-feature develop
   ```

2. **Make changes and commit**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   ```

4. **CI Pipeline runs automatically:**
   - Linting and formatting checks
   - Security scans
   - Full test suite
   - PR labeled automatically

5. **Review coverage report** (commented on PR)

6. **After approval and passing checks**, merge to `develop`

7. **Develop → Main** triggers deployment

## Automated Dependency Updates

**Dependabot Configuration:**
- Runs weekly (Monday 9:00 AM)
- Updates Python packages, GitHub Actions, Docker images
- Creates PRs automatically
- Grouped by ecosystem

**Review process:**
1. Dependabot creates PR
2. CI pipeline runs tests
3. Review changelog and compatibility
4. Merge if tests pass

## Troubleshooting

### Tests Failing in CI but Passing Locally

**Cause:** Environment differences (database, Python version, dependencies)

**Solutions:**
```bash
# Use same Python version as CI
pyenv install 3.11
pyenv local 3.11

# Run tests with PostgreSQL
docker-compose up -d postgres redis
export DATABASE_URL=postgresql://test_user:test_password@localhost:5432/quiz_app_test
pytest tests/

# Check dependency versions
pip list --outdated
```

### Docker Build Failing

**Common issues:**
- Missing requirements files
- Incorrect COPY paths in Dockerfile
- Build context too large (.dockerignore not configured)

**Debug:**
```bash
docker build -f deployment/docker/Dockerfile . --progress=plain
```

### Deployment Failing

**Check:**
1. SSH key is correctly configured
2. Server has sufficient resources
3. Database migrations are compatible
4. Environment variables are set

**Manual deployment:**
```bash
ssh user@server
cd /app/quiz-app
git pull origin main
docker-compose up -d --build
docker-compose exec web flask db upgrade
```

### Coverage Below Threshold

**Strategies:**
1. Add tests for uncovered code
2. Remove dead code
3. Adjust threshold temporarily: `--cov-fail-under=70`

## Performance Optimization

### Cache Configuration

**pip cache** is enabled in all workflows:
```yaml
- uses: actions/setup-python@v5
  with:
    cache: 'pip'
```

**Docker layer caching:**
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

### Parallel Jobs

Jobs run in parallel when possible:
- `lint`, `security`, `test` run simultaneously
- `integration-test` and `build` wait for dependencies

### Matrix Strategy

Tests run across multiple Python versions concurrently:
```yaml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11", "3.12"]
```

## Monitoring and Notifications

### Coverage Reports

- Uploaded to Codecov after each test run
- Commented on PRs with coverage diff
- View detailed reports at: `https://codecov.io/gh/YOUR-USERNAME/production-quiz-app`

### Security Alerts

- Trivy results uploaded to GitHub Security tab
- Dependabot alerts for vulnerable dependencies
- Bandit warnings in workflow artifacts

### Build Status

- Badges in README show current status
- GitHub Actions tab shows detailed logs
- Email notifications for failed workflows (configure in GitHub settings)

## Best Practices

1. **Always run tests locally before pushing**
   ```bash
   pytest tests/ && black app/ tests/ && isort app/ tests/
   ```

2. **Keep workflows fast:**
   - Use caching
   - Run expensive jobs only when needed
   - Parallelize independent jobs

3. **Fail fast:**
   - Critical checks (lint, tests) should fail immediately
   - Optional checks use `continue-on-error: true`

4. **Security first:**
   - Never commit secrets to repository
   - Use GitHub Secrets for sensitive data
   - Rotate credentials regularly

5. **Monitor costs:**
   - GitHub Actions has usage limits
   - Optimize workflow runs
   - Use `if` conditions to skip unnecessary jobs

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Codecov Documentation](https://docs.codecov.com/)
- [Docker Build Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot)

## Support

For issues with the CI/CD pipeline:
1. Check workflow logs in GitHub Actions tab
2. Review this documentation
3. Open an issue with the `ci-cd` label
