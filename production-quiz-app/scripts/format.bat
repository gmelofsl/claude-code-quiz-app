@echo off
REM Code formatting script for Production Quiz App (Windows)
REM Automatically fixes code formatting issues

echo === Auto-formatting Code ===
echo.

REM 1. Black - Format code
echo Running Black (code formatter)...
black app\ tests\
echo [OK] Code formatted with Black
echo.

REM 2. isort - Sort imports
echo Running isort (import sorter)...
isort app\ tests\
echo [OK] Imports sorted with isort
echo.

REM 3. Run linting to check if there are remaining issues
echo === Checking for remaining issues ===
echo.

set ERRORS=0

echo Running Flake8...
flake8 app\ tests\
if %ERRORLEVEL% EQU 0 (
    echo [OK] Flake8 passed
) else (
    echo [WARN] Flake8 found some issues (may require manual fixes)
    set /a ERRORS+=1
)
echo.

REM Summary
echo === Summary ===
if %ERRORS% EQU 0 (
    echo Code is now formatted and lint-free!
    echo.
    echo Don't forget to:
    echo   1. Review the changes: git diff
    echo   2. Stage the changes: git add .
    echo   3. Commit: git commit -m "style: format code"
) else (
    echo Code has been formatted, but some linting issues remain.
    echo Please review and fix them manually.
)
