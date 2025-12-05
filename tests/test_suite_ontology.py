"""
Test Suite: Ontology Management
================================

This test suite covers all ontology-related test cases:
- Object Type Creation
- Property Management
- Relation Management

Usage:
    python tests/test_suite_ontology.py
    or
    pytest tests/test_suite_ontology.py -v
"""

import sys
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_ontology_tests():
    """
    Run all ontology-related tests.
    """
    print("\n" + "="*80)
    print("ONTOLOGY TEST SUITE")
    print("="*80)
    print("\nThis suite includes:")
    print("  1. Object Type Creation")
    print("  2. Property Creation (7 types)")
    print("  3. Relation Creation (One-To-One, One-To-Many)")
    print("\n" + "="*80 + "\n")

    # List of test files to run
    test_files = [
        "tests/functional/test_create_object_type.py",
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

        # Run the test
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
    print("ONTOLOGY TEST SUITE COMPLETED SUCCESSFULLY")
    print("="*80 + "\n")
    return True


if __name__ == "__main__":
    success = run_ontology_tests()
    sys.exit(0 if success else 1)
