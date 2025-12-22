# CI/CD Quick Start Guide

## Setup Steps

### 1. Configure GitHub Secrets

Go to: `Settings > Secrets and Variables > Actions > New repository secret`

**Required:**
```
CODECOV_TOKEN=your_codecov_token
```

**For Docker (optional):**
```
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_token
```

**For Deployment (optional):**
```
DEPLOY_HOST=your.server.com
DEPLOY_USER=deploy
DEPLOY_SSH_KEY=your_private_ssh_key
DEPLOY_PORT=22
```

### 2. Update Badge URLs in README.md

Replace `YOUR-USERNAME` with your GitHub username:
```markdown
[![CI/CD Pipeline](https://github.com/YOUR-USERNAME/production-quiz-app/workflows/CI/CD%20Pipeline/badge.svg)]...
```

### 3. Update Dependabot Reviewers

Edit `.github/dependabot.yml`:
```yaml
reviewers:
  - "your-github-username"
```

### 4. Enable Branch Protection

Settings > Branches > Add rule for `main`:
- ✅ Require pull request reviews (1 approval)
- ✅ Require status checks: `lint`, `test`
- ✅ Require branches to be up to date

## Workflow Triggers

| Event | Workflows That Run |
|-------|-------------------|
| Push to `main` | Lint → Test → Build → Deploy |
| Push to `develop` | Lint → Test |
| Pull Request | Lint → Test → PR Label |
| Dependabot PR | Auto-created weekly |

## Local Testing

```bash
# Run what CI runs
black --check app/ tests/ scripts/
isort --check-only app/ tests/ scripts/
flake8 app/ tests/ scripts/
pytest tests/ -v --cov=app

# Auto-fix formatting
black app/ tests/ scripts/
isort app/ tests/ scripts/
```

## Viewing Results

- **Actions Tab**: All workflow runs
- **Pull Requests**: Coverage comments
- **Security Tab**: Vulnerability scans
- **Codecov**: Detailed coverage reports

## Common Commands

```bash
# Trigger CI manually
git commit --allow-empty -m "trigger ci"
git push

# Check workflow syntax
yamllint .github/workflows/*.yml

# Test Docker build locally
docker build -f deployment/docker/Dockerfile .
```

## Getting Help

- Check workflow logs in GitHub Actions tab
- Review [CICD.md](../CICD.md) for detailed documentation
- Open an issue with `ci-cd` label
