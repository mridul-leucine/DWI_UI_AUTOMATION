"""
Test Suite: Process Execution
==============================

This test suite covers all process execution related test cases:
- Process Search and Selection
- Job Creation
- Job Execution
- Parameter Filling (All 7 types)
- Task Completion
- Validation

Usage:
    python tests/test_suite_process_execution.py
    or
    pytest tests/test_suite_process_execution.py -v
"""

import sys
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_process_execution_tests():
    """
    Run all process execution related tests.
    """
    print("\n" + "="*80)
    print("PROCESS EXECUTION TEST SUITE")
    print("="*80)
    print("\nThis suite includes:")
    print("  1. Login and Facility Selection")
    print("  2. Process Search and Selection")
    print("  3. Job Creation")
    print("  4. Job Execution Start")
    print("  5. Parameter Filling (Number, Text, Date, Resource, Dropdown, YesNo, Image)")
    print("  6. Task Completion")
    print("  7. Validation")
    print("\n" + "="*80 + "\n")

    # List of test files to run
    test_files = [
        "tests/functional/test_qa_ui_all_para.py",
    ]

    # Run each test file
    for test_file in test_files:
        test_path = project_root / test_file

        if not test_path.exists():
            print(f"[WARNING] Test file not found: {test_file}")
            continue

        print(f"\n{'='*80}")
        print(f"Running: {test_file}")
        print(f"{'='*80}\n")

        # Check if it's a pytest file
        if "pytest" in open(test_path).read():
            # Run with pytest
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_path), "-v", "-s"],
                cwd=str(project_root),
                capture_output=False
            )
        else:
            # Run directly
            result = subprocess.run(
                [sys.executable, str(test_path)],
                cwd=str(project_root),
                capture_output=False
            )

        if result.returncode != 0:
            print(f"\n[ERROR] Test failed: {test_file}")
            return False
        else:
            print(f"\n[SUCCESS] Test passed: {test_file}")

    print("\n" + "="*80)
    print("PROCESS EXECUTION TEST SUITE COMPLETED SUCCESSFULLY")
    print("="*80 + "\n")
    return True


if __name__ == "__main__":
    success = run_process_execution_tests()
    sys.exit(0 if success else 1)
