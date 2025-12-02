@echo off
REM Test execution script for DWI UI Automation Framework
REM Run specific test suites or all tests with reporting

echo ================================
echo DWI UI Automation Test Runner
echo ================================
echo.

REM Check if virtual environment is activated
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please activate virtual environment.
    exit /b 1
)

REM Parse command line arguments
set TEST_TYPE=%1
if "%TEST_TYPE%"=="" set TEST_TYPE=all

echo Running tests: %TEST_TYPE%
echo.

REM Run tests based on type
if "%TEST_TYPE%"=="all" (
    echo Running all tests...
    pytest tests/
) else if "%TEST_TYPE%"=="smoke" (
    echo Running smoke tests...
    pytest tests/ -m smoke
) else if "%TEST_TYPE%"=="critical" (
    echo Running critical tests...
    pytest tests/ -m critical
) else if "%TEST_TYPE%"=="qa-ui-all-para" (
    echo Running qa-ui-all-para test...
    pytest tests/functional/test_qa_ui_all_para.py
) else if "%TEST_TYPE%"=="parallel" (
    echo Running tests in parallel...
    pytest tests/ -n auto
) else (
    echo Running specific test: %TEST_TYPE%
    pytest %TEST_TYPE%
)

echo.
echo ================================
echo Test execution completed
echo ================================
echo.
echo Reports generated:
echo - HTML Report: test-results\report.html
echo - Allure Results: test-results\allure-results\
echo - Logs: test-results\logs\
echo - Screenshots: test-results\screenshots\
echo.
echo To generate Allure HTML report, run:
echo   allure serve test-results\allure-results
echo.

pause
