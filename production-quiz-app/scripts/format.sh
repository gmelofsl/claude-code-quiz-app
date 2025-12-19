#!/bin/bash
# Code formatting script for Production Quiz App
# Automatically fixes code formatting issues

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Auto-formatting Code ===${NC}\n"

# 1. Black - Format code
echo -e "${YELLOW}Running Black (code formatter)...${NC}"
black app/ tests/
echo -e "${GREEN}✓ Code formatted with Black${NC}\n"

# 2. isort - Sort imports
echo -e "${YELLOW}Running isort (import sorter)...${NC}"
isort app/ tests/
echo -e "${GREEN}✓ Imports sorted with isort${NC}\n"

# 3. Run linting to check if there are remaining issues
echo -e "${BLUE}=== Checking for remaining issues ===${NC}\n"

ERRORS=0

# Check Flake8
echo -e "${YELLOW}Running Flake8...${NC}"
if flake8 app/ tests/; then
    echo -e "${GREEN}✓ Flake8 passed${NC}\n"
else
    echo -e "${YELLOW}⚠ Flake8 found some issues (may require manual fixes)${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Summary
echo -e "${BLUE}=== Summary ===${NC}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}Code is now formatted and lint-free! ✓${NC}"
    echo -e "\n${BLUE}Don't forget to:${NC}"
    echo -e "  1. Review the changes: ${YELLOW}git diff${NC}"
    echo -e "  2. Stage the changes: ${YELLOW}git add .${NC}"
    echo -e "  3. Commit: ${YELLOW}git commit -m 'style: format code'${NC}"
else
    echo -e "${YELLOW}Code has been formatted, but some linting issues remain.${NC}"
    echo -e "${YELLOW}Please review and fix them manually.${NC}"
fi
