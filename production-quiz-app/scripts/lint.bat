@echo off
REM Linting script for Production Quiz App (Windows)
REM Runs all code quality checks

echo === Running Code Quality Checks ===
echo.

set ERRORS=0

REM 1. Black - Code formatting check
echo Running Black (formatting)...
black --check app\ tests\
if %ERRORLEVEL% EQU 0 (
    echo [OK] Black passed
) else (
    echo [FAIL] Black failed
    set /a ERRORS+=1
)
echo.

REM 2. isort - Import sorting check
echo Running isort (imports)...
isort --check-only app\ tests\
if %ERRORLEVEL% EQU 0 (
    echo [OK] isort passed
) else (
    echo [FAIL] isort failed
    set /a ERRORS+=1
)
echo.

REM 3. Flake8 - Linting
echo Running Flake8 (linting)...
flake8 app\ tests\
if %ERRORLEVEL% EQU 0 (
    echo [OK] Flake8 passed
) else (
    echo [FAIL] Flake8 failed
    set /a ERRORS+=1
)
echo.

REM 4. Bandit - Security check
echo Running Bandit (security)...
bandit -r app\ -f json -o bandit-report.json
if %ERRORLEVEL% EQU 0 (
    echo [OK] Bandit passed
) else (
    echo [WARN] Bandit found some issues
)
echo.

REM Summary
echo === Summary ===
if %ERRORS% EQU 0 (
    echo All checks passed!
    exit /b 0
) else (
    echo %ERRORS% check(s) failed
    echo.
    echo To fix formatting issues automatically, run:
    echo   scripts\format.bat
    exit /b 1
)
