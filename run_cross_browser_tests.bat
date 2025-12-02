@echo off
REM Cross-browser test execution script
REM Runs tests on Chromium, Firefox, and WebKit browsers

echo ========================================
echo Cross-Browser Test Execution
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please activate virtual environment.
    exit /b 1
)

echo Installing browser drivers...
python -m playwright install chromium firefox webkit
echo.

echo ========================================
echo Running tests on CHROMIUM
echo ========================================
pytest tests/ --browser=chromium --html=test-results/report-chromium.html --self-contained-html -v
set chromium_result=%errorlevel%
echo.

echo ========================================
echo Running tests on FIREFOX
echo ========================================
pytest tests/ --browser=firefox --html=test-results/report-firefox.html --self-contained-html -v
set firefox_result=%errorlevel%
echo.

echo ========================================
echo Running tests on WEBKIT (Safari)
echo ========================================
pytest tests/ --browser=webkit --html=test-results/report-webkit.html --self-contained-html -v
set webkit_result=%errorlevel%
echo.

echo ========================================
echo Cross-Browser Test Summary
echo ========================================
echo.

if %chromium_result%==0 (
    echo [PASS] Chromium tests: PASSED
) else (
    echo [FAIL] Chromium tests: FAILED
)

if %firefox_result%==0 (
    echo [PASS] Firefox tests: PASSED
) else (
    echo [FAIL] Firefox tests: FAILED
)

if %webkit_result%==0 (
    echo [PASS] WebKit tests: PASSED
) else (
    echo [FAIL] WebKit tests: FAILED
)

echo.
echo Reports generated:
echo   - Chromium: test-results\report-chromium.html
echo   - Firefox:  test-results\report-firefox.html
echo   - WebKit:   test-results\report-webkit.html
echo.

REM Return non-zero if any browser failed
set /a total_failures=%chromium_result% + %firefox_result% + %webkit_result%
if %total_failures% gtr 0 (
    echo OVERALL RESULT: FAILED
    exit /b 1
) else (
    echo OVERALL RESULT: PASSED
    exit /b 0
)
