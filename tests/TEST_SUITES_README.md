# Test Suites Documentation

This document describes the available test suites and how to run them.

## Overview

The automation framework includes two main test suites:

### 1. Process Execution Test Suite
Tests the complete process execution workflow including:
- Login and facility selection
- Process search and selection
- Job creation and execution
- Parameter filling (7 types: Number, Text, Date, Resource, Dropdown, YesNo, Image)
- Task completion and validation

**Test File:** `test_suite_process_execution.py`

### 2. Ontology Management Test Suite
Tests the ontology management features including:
- Object type creation
- Property creation (7 parameter types)
- Relation creation (One-To-One, One-To-Many)

**Test File:** `test_suite_ontology.py`

### 3. Master Test Suite (All Tests)
Runs all test suites sequentially with detailed reporting.

**Test File:** `test_suite_all.py`

## How to Run

### Run Individual Test Suites

#### Process Execution Tests
```bash
# Run from project root
python tests/test_suite_process_execution.py

# Or with pytest
pytest tests/test_suite_process_execution.py -v
```

#### Ontology Management Tests
```bash
# Run from project root
python tests/test_suite_ontology.py

# Or with pytest
pytest tests/test_suite_ontology.py -v
```

#### All Tests (Master Suite)
```bash
# Run from project root
python tests/test_suite_all.py
```

### Run Individual Test Files Directly

#### Run Process Execution Test
```bash
python tests/functional/test_qa_ui_all_para.py
```

#### Run Object Type Creation Test
```bash
python tests/functional/test_create_object_type.py
```

## Test Suite Structure

```
tests/
├── test_suite_all.py                  # Master suite - runs all tests
├── test_suite_process_execution.py    # Process execution test suite
├── test_suite_ontology.py            # Ontology management test suite
├── TEST_SUITES_README.md             # This file
└── functional/
    ├── test_qa_ui_all_para.py        # Process execution test
    ├── test_create_object_type.py    # Object type creation test
    └── ...other tests...
```

## Test Results

Each test suite provides:
- Real-time console output with detailed logs
- Execution summary with pass/fail status
- Duration metrics
- Debug log files in `test-results/logs/`

## Adding New Tests

### To add a test to Process Execution Suite:
1. Create your test file in `tests/functional/`
2. Add the file path to `test_files` list in `test_suite_process_execution.py`

### To add a test to Ontology Suite:
1. Create your test file in `tests/functional/`
2. Add the file path to `test_files` list in `test_suite_ontology.py`

## Configuration

Test configuration is managed in:
- `data/credentials.json` - User credentials
- `data/config.json` - Browser and timeout settings
- `data/qa_ui_all_para_test_data.json` - Process test data

## Features

### Optimized Execution
- Minimal wait times (only for dropdown/search loading)
- No unnecessary screenshots
- Fast form filling with paste/fill operations
- Efficient parameter handling

### Comprehensive Coverage
- All 7 parameter types tested
- Multiple relation cardinalities
- Complete end-to-end workflows

### Detailed Logging
- Step-by-step execution logs
- Debug information for troubleshooting
- Timestamped log files

## Troubleshooting

If tests fail:
1. Check the debug log file in `test-results/logs/`
2. Verify credentials in `data/credentials.json`
3. Ensure the application is accessible
4. Check browser automation is working (slow_mo mode can help debug)

For more help, check the main project README or contact the automation team.
