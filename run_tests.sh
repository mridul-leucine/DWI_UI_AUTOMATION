#!/bin/bash
# Test execution script for DWI UI Automation Framework
# Run specific test suites or all tests with reporting

echo "================================"
echo "DWI UI Automation Test Runner"
echo "================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python not found. Please activate virtual environment."
    exit 1
fi

# Parse command line arguments
TEST_TYPE="${1:-all}"

echo "Running tests: $TEST_TYPE"
echo ""

# Run tests based on type
case "$TEST_TYPE" in
    "all")
        echo "Running all tests..."
        pytest tests/
        ;;
    "smoke")
        echo "Running smoke tests..."
        pytest tests/ -m smoke
        ;;
    "critical")
        echo "Running critical tests..."
        pytest tests/ -m critical
        ;;
    "qa-ui-all-para")
        echo "Running qa-ui-all-para test..."
        pytest tests/functional/test_qa_ui_all_para.py
        ;;
    "parallel")
        echo "Running tests in parallel..."
        pytest tests/ -n auto
        ;;
    *)
        echo "Running specific test: $TEST_TYPE"
        pytest "$TEST_TYPE"
        ;;
esac

echo ""
echo "================================"
echo "Test execution completed"
echo "================================"
echo ""
echo "Reports generated:"
echo "  - HTML Report: test-results/report.html"
echo "  - Allure Results: test-results/allure-results/"
echo "  - Logs: test-results/logs/"
echo "  - Screenshots: test-results/screenshots/"
echo ""
echo "To generate Allure HTML report, run:"
echo "  allure serve test-results/allure-results"
echo ""
