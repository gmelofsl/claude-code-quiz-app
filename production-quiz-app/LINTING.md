# Code Quality & Linting Guide

Comprehensive guide to code quality tools and linting in the Production Quiz App.

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Available Tools](#available-tools)
- [Configuration Files](#configuration-files)
- [Usage](#usage)
- [Pre-commit Hooks](#pre-commit-hooks)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

---

## Overview

The project uses multiple tools to ensure code quality:

- **Black**: Code formatting (opinionated, consistent)
- **isort**: Import sorting
- **Flake8**: Linting (PEP 8 compliance, code smells)
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checking
- **mypy**: Optional static type checking
- **pre-commit**: Automated hooks for git commits

---

## Quick Start

### Install Tools

```bash
# Install all development dependencies
pip install -r requirements/development.txt

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

### Run Linting

```bash
# Linux/Mac
./scripts/lint.sh

# Windows
scripts\lint.bat

# Docker
docker-compose exec web bash scripts/lint.sh
```

### Auto-fix Issues

```bash
# Linux/Mac
./scripts/format.sh

# Windows
scripts\format.bat

# Docker
docker-compose exec web bash scripts/format.sh
```

---

## Available Tools

### 1. Black - Code Formatter

**Purpose**: Automatically format Python code to a consistent style.

**Configuration**: `pyproject.toml`

**Run manually:**
```bash
# Check formatting
black --check app/ tests/

# Format code
black app/ tests/

# Format specific file
black app/models/user.py
```

**Key settings:**
- Line length: 100 characters
- Target: Python 3.11+
- Excludes: migrations, venv

### 2. isort - Import Sorter

**Purpose**: Sort and organize import statements.

**Configuration**: `pyproject.toml`

**Run manually:**
```bash
# Check imports
isort --check-only app/ tests/

# Sort imports
isort app/ tests/

# Sort specific file
isort app/models/user.py
```

**Import order:**
1. Standard library
2. Third-party packages
3. First-party (app, tests)
4. Local imports

### 3. Flake8 - Linter

**Purpose**: Check for PEP 8 compliance, code smells, and logical errors.

**Configuration**: `.flake8`

**Run manually:**
```bash
# Lint all code
flake8 app/ tests/

# Lint specific file
flake8 app/models/user.py

# Show statistics
flake8 app/ --statistics

# Show source code for errors
flake8 app/ --show-source
```

**Plugins included:**
- `flake8-docstrings`: Check docstring conventions
- `flake8-bugbear`: Find likely bugs and design problems
- `flake8-comprehensions`: Improve list/set/dict comprehensions
- `flake8-simplify`: Suggest code simplifications

**Key settings:**
- Max line length: 100 characters
- Max complexity: 10
- Ignores: E203, E501, W503 (compatible with Black)

### 4. Bandit - Security Scanner

**Purpose**: Find common security issues in Python code.

**Run manually:**
```bash
# Scan for security issues
bandit -r app/

# Generate JSON report
bandit -r app/ -f json -o bandit-report.json

# Exclude test files
bandit -r app/ -x tests/
```

**Common checks:**
- SQL injection vulnerabilities
- Hard-coded passwords
- Use of unsafe functions (eval, exec)
- Weak cryptography
- Command injection

### 5. Safety - Dependency Scanner

**Purpose**: Check for known security vulnerabilities in dependencies.

**Run manually:**
```bash
# Check dependencies
safety check

# Check specific requirements file
safety check -r requirements/base.txt

# Generate JSON report
safety check --json
```

### 6. mypy - Type Checker

**Purpose**: Optional static type checking for Python.

**Configuration**: `pyproject.toml`

**Run manually:**
```bash
# Type check all code
mypy app/

# Type check specific file
mypy app/models/user.py

# Strict mode
mypy app/ --strict
```

**Note**: Type checking is optional but recommended for new code.

---

## Configuration Files

### pyproject.toml

Central configuration for:
- Black (formatting)
- isort (imports)
- pytest (testing)
- coverage (test coverage)
- mypy (type checking)

**Key sections:**
```toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.11"
warn_return_any = true
```

### .flake8

Configuration for Flake8 linter:
```ini
[flake8]
max-line-length = 100
max-complexity = 10
exclude = .git,__pycache__,.venv,migrations
```

### .pre-commit-config.yaml

Configuration for pre-commit hooks:
- Runs checks before git commit
- Automatically fixes some issues
- Blocks commit if checks fail

---

## Usage

### Command Line

**Check everything:**
```bash
./scripts/lint.sh          # Linux/Mac
scripts\lint.bat           # Windows
```

**Auto-fix formatting:**
```bash
./scripts/format.sh        # Linux/Mac
scripts\format.bat         # Windows
```

**Individual tools:**
```bash
black --check app/         # Check formatting
black app/                 # Fix formatting
isort --check-only app/    # Check imports
isort app/                 # Fix imports
flake8 app/                # Lint code
bandit -r app/             # Security scan
mypy app/                  # Type check
```

### Docker

```bash
# Run linting in Docker
docker-compose exec web bash scripts/lint.sh

# Format code in Docker
docker-compose exec web bash scripts/format.sh

# Individual tools
docker-compose exec web black --check app/
docker-compose exec web flake8 app/
```

### IDE Integration

#### VS Code

Install extensions:
- Python (Microsoft)
- Black Formatter
- Flake8
- isort

**Settings (.vscode/settings.json):**
```json
{
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=100"],
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Args": ["--max-line-length=100"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

#### PyCharm

1. Go to **Settings → Tools → Black**
   - Enable Black formatter
   - Set line length: 100

2. Go to **Settings → Editor → Code Style → Python**
   - Import tab → Configure isort

3. Go to **Settings → Tools → External Tools**
   - Add Flake8 as external tool

---

## Pre-commit Hooks

Pre-commit hooks run automatically before each git commit.

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Install hooks in git repository
pre-commit install

# Install for commit messages
pre-commit install --hook-type commit-msg
```

### Usage

**Automatic (on commit):**
```bash
git commit -m "Add new feature"
# Pre-commit hooks run automatically
# Commit proceeds if all checks pass
```

**Manual run:**
```bash
# Run on all files
pre-commit run --all-files

# Run on staged files only
pre-commit run

# Run specific hook
pre-commit run black
pre-commit run flake8
```

**Update hooks:**
```bash
pre-commit autoupdate
```

**Skip hooks (emergency only):**
```bash
git commit -m "Emergency fix" --no-verify
```

### Hooks Enabled

1. **trailing-whitespace**: Remove trailing whitespace
2. **end-of-file-fixer**: Ensure files end with newline
3. **check-yaml**: Validate YAML syntax
4. **check-json**: Validate JSON syntax
5. **check-added-large-files**: Prevent large file commits
6. **debug-statements**: Detect forgotten debug statements
7. **detect-private-key**: Prevent committing private keys
8. **black**: Format code
9. **isort**: Sort imports
10. **flake8**: Lint code
11. **bandit**: Security scan
12. **pyupgrade**: Upgrade Python syntax

---

## CI/CD Integration

Linting runs automatically in GitHub Actions CI/CD pipeline.

### CI Pipeline (.github/workflows/ci.yml)

**Lint job:**
```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run Black
      run: black --check .
    - name: Run isort
      run: isort --check-only .
    - name: Run Flake8
      run: flake8 app/ tests/
```

**Security job:**
```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - name: Run Bandit
      run: bandit -r app/
    - name: Run Safety
      run: safety check
```

**Checks run on:**
- Every push to main/develop
- Every pull request
- Blocks merge if checks fail

---

## Troubleshooting

### Black and Flake8 Conflicts

**Problem**: Flake8 complains about formatting that Black enforces.

**Solution**: Configured to ignore conflicting rules:
```ini
[flake8]
ignore = E203, E501, W503
```

### Import Sorting Issues

**Problem**: isort and Black disagree on import formatting.

**Solution**: isort configured with Black profile:
```toml
[tool.isort]
profile = "black"
```

### Line Length Conflicts

**Problem**: Different tools use different line lengths.

**Solution**: All tools configured to 100 characters:
```toml
[tool.black]
line-length = 100

[tool.isort]
line_length = 100
```

```ini
[flake8]
max-line-length = 100
```

### Pre-commit Hook Failures

**Problem**: Pre-commit hooks fail and block commit.

**Solution 1 - Fix issues:**
```bash
# Run format script
./scripts/format.sh

# Re-stage files
git add .

# Try commit again
git commit -m "Your message"
```

**Solution 2 - Skip (emergency only):**
```bash
git commit -m "Emergency fix" --no-verify
```

### Bandit False Positives

**Problem**: Bandit reports non-issues as vulnerabilities.

**Solution**: Add `# nosec` comment:
```python
# Safe use of assert in tests
assert user.check_password("password")  # nosec
```

Or exclude in pyproject.toml:
```toml
[tool.bandit]
exclude_dirs = ["tests"]
```

---

## Best Practices

### 1. Run Before Committing

Always run linting before creating a commit:
```bash
./scripts/lint.sh
```

### 2. Use Auto-formatting

Let tools fix issues automatically:
```bash
./scripts/format.sh
```

### 3. Install Pre-commit Hooks

Catch issues early:
```bash
pre-commit install
```

### 4. Run in CI/CD

Enforce standards in pipeline (already configured).

### 5. Fix Issues Promptly

Don't accumulate linting debt. Fix issues as they appear.

### 6. Review Security Warnings

Take Bandit warnings seriously, especially:
- SQL injection risks
- Command injection
- Hard-coded secrets
- Weak cryptography

---

## Command Reference

### Quick Commands

```bash
# Check everything
./scripts/lint.sh

# Fix formatting
./scripts/format.sh

# Individual checks
black --check app/         # Format check
isort --check-only app/    # Import check
flake8 app/                # Lint
bandit -r app/             # Security
mypy app/                  # Type check

# Individual fixes
black app/                 # Format
isort app/                 # Sort imports

# Pre-commit
pre-commit run --all-files # Run all hooks
pre-commit install         # Install hooks
```

### Docker Commands

```bash
docker-compose exec web bash scripts/lint.sh
docker-compose exec web bash scripts/format.sh
docker-compose exec web black --check app/
docker-compose exec web flake8 app/
```

---

## Additional Resources

- **Black**: https://black.readthedocs.io/
- **isort**: https://pycqa.github.io/isort/
- **Flake8**: https://flake8.pycqa.org/
- **Bandit**: https://bandit.readthedocs.io/
- **Safety**: https://pyup.io/safety/
- **mypy**: https://mypy.readthedocs.io/
- **pre-commit**: https://pre-commit.com/

---

**Last Updated**: 2024-12-19
**Maintained By**: Production Quiz App Team
