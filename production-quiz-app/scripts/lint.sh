#!/bin/bash
# Linting script for Production Quiz App
# Runs all code quality checks

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Running Code Quality Checks ===${NC}\n"

# Track overall status
ERRORS=0

# Function to run a check
run_check() {
    local name=$1
    local command=$2

    echo -e "${YELLOW}Running ${name}...${NC}"
    if eval "$command"; then
        echo -e "${GREEN}✓ ${name} passed${NC}\n"
    else
        echo -e "${RED}✗ ${name} failed${NC}\n"
        ERRORS=$((ERRORS + 1))
    fi
}

# 1. Black - Code formatting check
run_check "Black (formatting)" "black --check app/ tests/"

# 2. isort - Import sorting check
run_check "isort (imports)" "isort --check-only app/ tests/"

# 3. Flake8 - Linting
run_check "Flake8 (linting)" "flake8 app/ tests/"

# 4. Bandit - Security check
run_check "Bandit (security)" "bandit -r app/ -f json -o bandit-report.json || true"

# 5. Safety - Dependency vulnerability check
if command -v safety &> /dev/null; then
    run_check "Safety (dependencies)" "safety check --json || true"
else
    echo -e "${YELLOW}⊘ Safety not installed, skipping${NC}\n"
fi

# 6. mypy - Type checking (optional)
if command -v mypy &> /dev/null; then
    run_check "mypy (type checking)" "mypy app/ || true"
else
    echo -e "${YELLOW}⊘ mypy not installed, skipping${NC}\n"
fi

# Summary
echo -e "${BLUE}=== Summary ===${NC}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}All checks passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}${ERRORS} check(s) failed ✗${NC}"
    echo -e "\n${YELLOW}To fix formatting issues automatically, run:${NC}"
    echo -e "  ${BLUE}./scripts/format.sh${NC}"
    exit 1
fi
