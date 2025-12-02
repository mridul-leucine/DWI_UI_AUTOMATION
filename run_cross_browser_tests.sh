#!/bin/bash
# Cross-browser test execution script
# Runs tests on Chromium, Firefox, and WebKit browsers

echo "========================================"
echo "Cross-Browser Test Execution"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python not found. Please activate virtual environment."
    exit 1
fi

echo "Installing browser drivers..."
python -m playwright install chromium firefox webkit
echo ""

echo "========================================"
echo "Running tests on CHROMIUM"
echo "========================================"
pytest tests/ --browser=chromium --html=test-results/report-chromium.html --self-contained-html -v
chromium_result=$?
echo ""

echo "========================================"
echo "Running tests on FIREFOX"
echo "========================================"
pytest tests/ --browser=firefox --html=test-results/report-firefox.html --self-contained-html -v
firefox_result=$?
echo ""

echo "========================================"
echo "Running tests on WEBKIT (Safari)"
echo "========================================"
pytest tests/ --browser=webkit --html=test-results/report-webkit.html --self-contained-html -v
webkit_result=$?
echo ""

echo "========================================"
echo "Cross-Browser Test Summary"
echo "========================================"
echo ""

if [ $chromium_result -eq 0 ]; then
    echo "[PASS] Chromium tests: PASSED"
else
    echo "[FAIL] Chromium tests: FAILED"
fi

if [ $firefox_result -eq 0 ]; then
    echo "[PASS] Firefox tests: PASSED"
else
    echo "[FAIL] Firefox tests: FAILED"
fi

if [ $webkit_result -eq 0 ]; then
    echo "[PASS] WebKit tests: PASSED"
else
    echo "[FAIL] WebKit tests: FAILED"
fi

echo ""
echo "Reports generated:"
echo "  - Chromium: test-results/report-chromium.html"
echo "  - Firefox:  test-results/report-firefox.html"
echo "  - WebKit:   test-results/report-webkit.html"
echo ""

# Return non-zero if any browser failed
total_failures=$((chromium_result + firefox_result + webkit_result))
if [ $total_failures -gt 0 ]; then
    echo "OVERALL RESULT: FAILED"
    exit 1
else
    echo "OVERALL RESULT: PASSED"
    exit 0
fi
