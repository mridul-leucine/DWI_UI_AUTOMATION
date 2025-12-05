"""
Master Test Suite: All Tests
=============================

This master test suite runs all test suites:
1. Process Execution Test Suite
2. Ontology Management Test Suite

Usage:
    python tests/test_suite_all.py
    or
    pytest tests/ -v
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_all_test_suites():
    """
    Run all test suites sequentially.
    """
    start_time = datetime.now()

    print("\n" + "="*80)
    print("MASTER TEST SUITE - ALL TESTS")
    print("="*80)
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "="*80 + "\n")

    # Test suites to run
    test_suites = [
        {
            "name": "Process Execution Test Suite",
            "file": "tests/test_suite_process_execution.py",
            "description": "Tests for process search, job creation, execution, and parameter filling"
        },
        {
            "name": "Ontology Management Test Suite",
            "file": "tests/test_suite_ontology.py",
            "description": "Tests for object type, property, and relation creation"
        }
    ]

    results = []

    # Run each test suite
    for idx, suite in enumerate(test_suites, 1):
        suite_path = project_root / suite["file"]

        print(f"\n{'='*80}")
        print(f"TEST SUITE {idx}/{len(test_suites)}: {suite['name']}")
        print(f"{'='*80}")
        print(f"Description: {suite['description']}")
        print(f"File: {suite['file']}")
        print(f"{'='*80}\n")

        if not suite_path.exists():
            print(f"[WARNING] Test suite file not found: {suite['file']}")
            results.append({
                "suite": suite["name"],
                "status": "SKIPPED",
                "reason": "File not found"
            })
            continue

        # Run the test suite
        suite_start = datetime.now()
        result = subprocess.run(
            [sys.executable, str(suite_path)],
            cwd=str(project_root),
            capture_output=False
        )
        suite_duration = (datetime.now() - suite_start).total_seconds()

        if result.returncode != 0:
            print(f"\n[ERROR] Test suite failed: {suite['name']}")
            results.append({
                "suite": suite["name"],
                "status": "FAILED",
                "duration": suite_duration
            })
        else:
            print(f"\n[SUCCESS] Test suite passed: {suite['name']}")
            results.append({
                "suite": suite["name"],
                "status": "PASSED",
                "duration": suite_duration
            })

    # Print summary
    end_time = datetime.now()
    total_duration = (end_time - start_time).total_seconds()

    print("\n" + "="*80)
    print("TEST EXECUTION SUMMARY")
    print("="*80)
    print(f"Start Time:    {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End Time:      {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Duration: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")
    print("\n" + "-"*80)

    passed = sum(1 for r in results if r["status"] == "PASSED")
    failed = sum(1 for r in results if r["status"] == "FAILED")
    skipped = sum(1 for r in results if r["status"] == "SKIPPED")

    for idx, result in enumerate(results, 1):
        status_symbol = "✓" if result["status"] == "PASSED" else "✗" if result["status"] == "FAILED" else "⊘"
        duration_text = f"({result['duration']:.2f}s)" if "duration" in result else ""
        print(f"{idx}. {status_symbol} {result['suite']}: {result['status']} {duration_text}")

    print("-"*80)
    print(f"\nTotal Suites: {len(results)}")
    print(f"Passed:       {passed}")
    print(f"Failed:       {failed}")
    print(f"Skipped:      {skipped}")
    print("="*80 + "\n")

    # Return success if all passed
    return failed == 0


if __name__ == "__main__":
    success = run_all_test_suites()
    sys.exit(0 if success else 1)
