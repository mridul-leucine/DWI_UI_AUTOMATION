# DWI UI Automation Framework

**Production-ready** Python + Playwright automation framework for testing DWI platform processes.

Built with **reusability, scalability, and maintainability** as core principles.

## Table of Contents
- [Framework Architecture](#framework-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Data Management](#test-data-management)
- [Reporting](#reporting)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Framework Architecture

### 🎯 Core Principles
- **Reusability**: BasePage class with common functionality - write once, use everywhere
- **Scalability**: Easy to add new tests and page objects
- **Maintainability**: Centralized constants, clear structure, explicit over implicit
- **DRY**: Don't Repeat Yourself - single source of truth for all configurations

### 🏗️ Key Components

#### 1. BasePage (`pom/base_page.py`)
All page objects inherit from `BasePage`, providing:
- **Navigation**: `navigate_to()`, `get_current_url()`, `wait_for_load_state()`
- **Element Interaction**: `click_element()`, `fill_input()`, `get_text()`
- **Waits**: `wait_for_element()`, `wait_for_timeout()`
- **Validation**: `is_element_visible()`, `verify_url_contains()`
- **Utilities**: `take_screenshot()`, `scroll_to_element()`, `refresh_page()`

#### 2. Constants (`pom/constants.py`)
Centralized configuration:
- **Timeouts**: `Timeouts.DEFAULT`, `Timeouts.NAVIGATION`, `Timeouts.ELEMENT`
- **Locator Strategies**: Common locator patterns
- **UI Messages**: Standard UI messages for validation
- **Paths**: File and directory paths
- **Parameter Types**: All parameter type constants

#### 3. Page Objects
Each page inherits from `BasePage` and adds page-specific functionality:
```python
from pom.base_page import BasePage
from pom.constants import Timeouts

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Page-specific logic
```

### ✨ Benefits
- **Write less code**: Common functionality in one place
- **Easier debugging**: Consistent patterns across all tests
- **Faster test development**: Reuse existing components
- **Better maintainability**: Change once, apply everywhere

## Prerequisites

- **Python**: 3.10+ (tested with 3.13.3)
- **pip**: Latest version
- **Git**: For version control
- **OS**: Windows, macOS, or Linux

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd dwi_playwright_automation
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers
```bash
python -m playwright install chromium
python -m playwright install firefox  # Optional
python -m playwright install webkit   # Optional
```

### 5. Setup test resources
Add a sample test image for upload testing:
```bash
# Place a test image file in:
test-resources/images/sample-test-image.jpg
```

## Project Structure

```
dwi_playwright_automation/
│
├── pom/                          # Page Object Model
│   ├── base_page.py              # ⭐ Base class for all pages (NEW)
│   ├── constants.py              # ⭐ Centralized constants (NEW)
│   ├── login.py                  # Login page
│   ├── facility_selection.py    # Facility selection page
│   ├── home_page.py              # Home page with use case selection
│   ├── process_list_page.py     # Process list page
│   ├── job_creation_page.py     # Job creation modal
│   ├── job_execution_page.py    # Job execution page
│   ├── ontology_page.py          # ⭐ Ontology management (NEW)
│   ├── sidebar.py                # ⭐ Sidebar navigation (NEW)
│   ├── task_navigation_panel.py # Task navigation panel
│   ├── parameter_panel.py       # Parameter panel base
│   └── components/              # Parameter components
│       ├── number_parameter.py
│       ├── single_line_parameter.py
│       ├── date_parameter.py
│       ├── resource_parameter.py
│       ├── single_select_parameter.py
│       ├── yesno_parameter.py
│       └── media_parameter.py
│
├── tests/
│   ├── functional/
│   │   ├── test_qa_ui_all_para.py          # Process execution test (7 params)
│   │   └── test_create_object_type.py      # ⭐ Ontology management test (NEW)
│   ├── test_suite_all.py                   # ⭐ Run all tests (NEW)
│   ├── test_suite_process_execution.py     # ⭐ Process suite (NEW)
│   └── test_suite_ontology.py              # ⭐ Ontology suite (NEW)
│
├── utils/                        # Utility modules
│   ├── test_data_manager.py     # Test data management
│   ├── wait_helper.py            # Wait utilities
│   ├── screenshot_helper.py     # Screenshot capture
│   └── logger.py                 # Logging utilities
│
├── data/                         # Test data
│   ├── credentials.json          # User credentials
│   ├── config.json               # Configuration
│   └── qa_ui_all_para_test_data.json  # Process test data
│
├── test-resources/               # Test assets
│   └── images/                   # Test images
│
├── test-results/                 # Test output (auto-generated)
│   ├── screenshots/              # Screenshots
│   ├── logs/                     # Log files
│   └── videos/                   # Recorded videos (optional)
│
├── conftest.py                   # Pytest configuration
├── pytest.ini                    # Pytest settings
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Configuration

### 1. Update credentials
Edit `data/credentials.json`:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

### 2. Configure settings
Edit `data/config.json` to customize:
- Base URL
- Timeouts
- Browser settings
- Screenshot settings

### 3. Update test data
Edit `data/qa_ui_all_para_test_data.json` for process-specific data:
- Facility name
- Use case
- Process code
- Parameter values

## Running Tests

### Quick Start with Test Runner Scripts

**Windows:**
```cmd
# Run all tests
run_tests.bat all

# Run specific test suite
run_tests.bat qa-ui-all-para
run_tests.bat smoke
run_tests.bat critical

# Run tests in parallel
run_tests.bat parallel
```

**Linux/macOS:**
```bash
# Run all tests
./run_tests.sh all

# Run specific test suite
./run_tests.sh qa-ui-all-para
./run_tests.sh smoke
./run_tests.sh critical

# Run tests in parallel
./run_tests.sh parallel
```

### Run with pytest directly

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/functional/test_qa_ui_all_para.py

# Run with markers
pytest -m smoke          # Smoke tests only
pytest -m critical       # Critical tests only

# Run in headless mode
pytest --headless

# Run with video recording
pytest --record-video

# Run in parallel (faster)
pytest -n auto

# Run with specific browser
pytest --browser=firefox
pytest --browser=webkit

# Run directly (without pytest)
python tests/functional/test_qa_ui_all_para.py
```

### IDE Integration

**VS Code:**
1. Install Python extension
2. Install Playwright Test extension (optional)
3. Open Test Explorer
4. Select pytest as test framework
5. Run/Debug tests from Test Explorer

**PyCharm:**
1. Configure pytest as default test runner
2. Right-click test file → Run/Debug
3. Use run configurations for custom parameters

**Command Palette:**
```
Python: Configure Tests → pytest → tests directory
```

## Test Data Management

The framework uses JSON files for test data management:

- **credentials.json**: User authentication
- **config.json**: Environment and browser configuration
- **qa_ui_all_para_test_data.json**: Process-specific test data

You can create additional test data files for different processes by following the same structure.

## Reporting

### HTML Report
After test execution, view the HTML report:
```
test-results/report.html
```

Open in browser:
```bash
# Windows
start test-results/report.html

# macOS
open test-results/report.html

# Linux
xdg-open test-results/report.html
```

### Allure Report
Generate and view Allure report:
```bash
# Generate HTML report
allure generate test-results/allure-results -o test-results/allure-report --clean

# Serve report (opens in browser)
allure serve test-results/allure-results
```

### Screenshots
Screenshots are automatically captured:
- On test failure (automatic via pytest hook)
- Manual capture during test execution
- Full page screenshots by default

Located in: `test-results/screenshots/`

Format: `{test_name}_{step_name}_{timestamp}.png`

### Logs
Detailed logs are available at:
- **Console**: INFO level (real-time feedback)
- **File**: DEBUG level in `test-results/logs/`

Log format: `test_execution_{timestamp}.log`

Includes:
- Timestamp for each action
- Test steps with descriptions
- Parameter values filled
- Verification results
- Error details with stack traces

### Video Recording
Enable with `--record-video` flag:
```bash
pytest --record-video
```
Videos saved to: `test-results/videos/`

**Note**: Videos are only kept for failed tests by default to save disk space.

## Troubleshooting

### Common Issues

#### 1. Element not found
**Problem**: Locator cannot find element
**Solutions**:
- Check if page is fully loaded
- Verify locator strategy (ID, class, text)
- Increase timeout in `config.json`
- Use explicit waits

#### 2. Timeout errors
**Problem**: Operations exceed timeout limit
**Solutions**:
- Increase default timeout in config
- Check network connectivity
- Verify application performance

#### 3. Stale element exception
**Problem**: Element reference becomes stale
**Solutions**:
- Re-locate element before interaction
- Use wait helpers from `utils/wait_helper.py`
- Refresh page object

#### 4. File upload fails
**Problem**: Image upload doesn't work
**Solutions**:
- Verify file exists in `test-resources/images/`
- Check file path is absolute
- Ensure file format is supported

#### 5. Test data not loaded
**Problem**: Test data files not found
**Solutions**:
- Verify file paths are correct
- Check JSON syntax
- Ensure files are in `data/` directory

### Debug Mode

Enable verbose logging:
```bash
pytest -v -s --log-cli-level=DEBUG
```

Capture screenshot at specific point:
```python
from utils.screenshot_helper import ScreenshotHelper

screenshot_helper = ScreenshotHelper(page)
screenshot_helper.capture_screenshot("my_test", "debug_step")
```

## Browser Support

The framework supports multiple browsers:

- **Chromium** (default, recommended)
- **Firefox**
- **WebKit** (Safari)

Switch browser:
```bash
pytest --browser=firefox
```

## Cross-Browser Testing

Run tests on all browsers:
```bash
pytest --browser=chromium
pytest --browser=firefox
pytest --browser=webkit
```

## Test Data Cleanup

### Cleaning Test Artifacts

```bash
# Clean all test artifacts
python cleanup.py --all

# Clean specific artifacts
python cleanup.py --screenshots    # Old screenshots
python cleanup.py --logs           # Old logs
python cleanup.py --videos         # All videos
python cleanup.py --cache          # Pytest cache
python cleanup.py --pycache        # Python cache
python cleanup.py --jobs           # Job tracking data
```

### Cleaning Test Jobs

The framework tracks test jobs created during execution. To manage test jobs:

```python
# In your test
from utils.job_cleanup import JobCleanup

job_cleanup = JobCleanup(page)
job_cleanup.register_job(job_code, test_name="test_example")

# Clean up after test
job_cleanup.cleanup_all_registered_jobs()
```

For detailed information, see `utils/JOB_CLEANUP_README.md`

## Continuous Integration (CI/CD)

### GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/test-execution.yml`) that:
- Runs tests on multiple Python versions (3.10, 3.11, 3.12)
- Tests across browsers (Chromium, Firefox)
- Generates and uploads test reports
- Captures screenshots on failure
- Runs smoke tests separately

**Trigger CI:**
```bash
# Push to main/develop branches
git push origin main

# Create pull request
gh pr create

# Manual trigger via GitHub UI
```

**View Results:**
- Go to GitHub Actions tab
- Select workflow run
- Download artifacts (reports, screenshots)

### Jenkins Integration

To integrate with Jenkins:
1. Install Python and Playwright on Jenkins agent
2. Create pipeline job
3. Use provided test scripts:
```groovy
stage('Test') {
    steps {
        sh './run_tests.sh all'
    }
}
```

### Local CI Simulation

Run tests in CI mode locally:
```bash
# Headless, parallel, with all reports
pytest --headless -n auto --alluredir=test-results/allure-results
```

## Contributing

### Coding Standards
- Follow PEP 8 style guide
- Use type hints where applicable
- Add docstrings to all classes and methods
- Keep methods focused and single-purpose

### Naming Conventions
- **Page Objects**: `<PageName>Page` (e.g., `LoginPage`)
- **Test Files**: `test_<feature>.py`
- **Test Methods**: `test_<scenario>()`
- **Locators**: Descriptive names (e.g., `username_input`)

### Adding New Tests
1. Create page objects in `pom/`
2. Add test data in `data/`
3. Write test in `tests/functional/`
4. Add assertions and validations
5. Update documentation

### Pull Request Process
1. Create feature branch
2. Write tests
3. Ensure all tests pass
4. Update README if needed
5. Submit PR with description

## Utility Modules

### Test Data Manager
```python
from utils.test_data_manager import get_test_data_manager

data_mgr = get_test_data_manager()
credentials = data_mgr.get_credentials()
test_data = data_mgr.get_test_data()
param_value = data_mgr.get_parameter_value("Number")
```

### Wait Helper
```python
from utils.wait_helper import WaitHelper

wait_helper = WaitHelper(page)
wait_helper.wait_for_element_visible(locator)
wait_helper.wait_for_element_clickable(locator)
wait_helper.custom_wait(lambda: condition_met(), timeout=5000)
```

### Screenshot Helper
```python
from utils.screenshot_helper import ScreenshotHelper

screenshot = ScreenshotHelper(page)
screenshot.capture_screenshot("test_name", "step_name")
screenshot.capture_on_failure("test_name", error_message)
```

### Logger
```python
from utils.logger import get_logger

logger = get_logger()
logger.info("Test step executed")
logger.error("Error occurred", exception=e)
logger.log_parameter_fill("Number", "123")
```

## Quick Reference

### Common Commands
```bash
# Setup
pip install -r requirements.txt
python -m playwright install chromium

# Run tests
pytest tests/
./run_tests.sh all

# View reports
allure serve test-results/allure-results
start test-results/report.html

# Cleanup
python cleanup.py --all
```

### Project Shortcuts
- Main test: `tests/functional/test_qa_ui_all_para.py`
- Test data: `data/qa_ui_all_para_test_data.json`
- Configuration: `data/config.json`
- Credentials: `data/credentials.json`
- Test results: `test-results/`

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review test logs in `test-results/logs/`
- Check GitHub Issues (if applicable)
- Review utility documentation in `utils/`
- Contact automation team

## License

Internal use only - TNN Technologies Private Limited

---

**Last Updated**: December 2025
**Framework Version**: 1.0.0
**Python Version**: 3.13.3
**Playwright Version**: 1.55.0
