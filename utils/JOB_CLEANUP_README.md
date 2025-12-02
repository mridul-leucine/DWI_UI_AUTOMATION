# Job Cleanup Utility

## Overview

The Job Cleanup utility provides mechanisms to clean up test jobs created during automated test execution in the DWI platform.

## Features

- **Job Registration**: Track test jobs created during execution
- **Multiple Cleanup Strategies**:
  - UI-based cleanup (navigate and delete via UI)
  - API-based cleanup (use REST APIs)
  - Database cleanup (direct database operations)
- **Automatic Tracking**: Jobs stored in `test-results/test_jobs.json`
- **Batch Cleanup**: Clean up multiple jobs at once

## Usage

### 1. Register Jobs During Tests

In your test code, register jobs for cleanup:

```python
from utils.job_cleanup import JobCleanup

# In your test
job_cleanup = JobCleanup(page)
job_cleanup.register_job(
    job_code="TEST-12345",
    test_name="test_qa_ui_all_para",
    additional_info={"process": "qa-ui-all para"}
)
```

### 2. Clean Up Jobs After Tests

#### Option A: Programmatic Cleanup

```python
from utils.job_cleanup import JobCleanup

# UI-based cleanup
cleanup = JobCleanup(page, cleanup_strategy="ui")
cleanup.cleanup_all_registered_jobs()

# API-based cleanup (if APIs available)
cleanup = JobCleanup(cleanup_strategy="api")
cleanup.cleanup_job_via_api(
    job_code="TEST-12345",
    base_url="https://api.example.com",
    auth_token="your-token"
)
```

#### Option B: Pytest Fixture Integration

Add to your `conftest.py`:

```python
from utils.job_cleanup import cleanup_test_jobs

@pytest.fixture(scope="session", autouse=True)
def cleanup_jobs_after_session(request):
    """Cleanup all test jobs after test session."""
    yield

    # Get page from somewhere or create temporary browser
    # cleanup_test_jobs(page)
    pass
```

#### Option C: Manual Cleanup

Run cleanup script:

```bash
# Clean up test jobs tracking
python cleanup.py --jobs

# Clean up everything
python cleanup.py --all
```

### 3. View Registered Jobs

```python
from utils.job_cleanup import JobCleanup

cleanup = JobCleanup()
jobs = cleanup.get_registered_jobs()

for job in jobs:
    print(f"Job: {job['job_code']}, Created: {job['created_at']}")
```

## Cleanup Strategies

### UI-Based Cleanup (Recommended)

Most reliable option when APIs are not available:

```python
cleanup = JobCleanup(page, cleanup_strategy="ui")
cleanup.cleanup_all_registered_jobs()
```

**Pros:**
- Works without API access
- Uses existing UI functionality
- No special permissions required

**Cons:**
- Slower than API
- Depends on UI stability
- Requires page object

### API-Based Cleanup

Fastest option if APIs are available:

```python
cleanup = JobCleanup(cleanup_strategy="api")
cleanup.cleanup_job_via_api(
    job_code="TEST-12345",
    base_url="https://api.example.com",
    auth_token="token"
)
```

**Pros:**
- Fast and efficient
- No UI interaction needed
- Can run headless

**Cons:**
- Requires API access
- May need special permissions
- API endpoint must exist

### Database Cleanup

Direct database operations (use with caution):

```sql
-- Example SQL for database cleanup
DELETE FROM jobs
WHERE code LIKE 'TEST-%'
AND created_at < NOW() - INTERVAL '7 days';
```

**Pros:**
- Very fast
- Direct data removal
- No dependency on UI/API

**Cons:**
- Requires database access
- Can be dangerous if misconfigured
- May violate data integrity

## File Structure

```
test-results/
└── test_jobs.json        # Tracking file for test jobs
```

### test_jobs.json Format

```json
{
  "jobs": [
    {
      "job_code": "TEST-20241201-153045",
      "test_name": "test_qa_ui_all_para",
      "created_at": "2024-12-01T15:30:45.123456",
      "additional_info": {
        "process": "qa-ui-all para",
        "facility": "Test Facility"
      }
    }
  ]
}
```

## Best Practices

1. **Always Register Jobs**: Register every test job created
2. **Clean Up Regularly**: Run cleanup after test sessions
3. **Use Prefixes**: Use identifiable prefixes for test jobs (e.g., "TEST-")
4. **Monitor Tracking File**: Check `test_jobs.json` periodically
5. **Choose Right Strategy**: Use UI cleanup for reliability, API for speed

## Integration Example

```python
# In test_qa_ui_all_para.py
from utils.job_cleanup import JobCleanup

def test_complete_process_execution(self, browser_setup):
    browser, page = browser_setup
    job_cleanup = JobCleanup(page)

    try:
        # Create job
        job_code = job_execution_page.get_job_code()

        # Register for cleanup
        job_cleanup.register_job(
            job_code=job_code,
            test_name="test_complete_process_execution"
        )

        # Rest of test...

    finally:
        # Cleanup in teardown
        job_cleanup.cleanup_all_registered_jobs()
```

## Troubleshooting

### Jobs Not Cleaning Up

1. Check if delete button selectors are correct
2. Verify page object is valid
3. Check for permission issues
4. Review error messages in console

### Tracking File Issues

1. Ensure `test-results/` directory exists
2. Check file permissions
3. Verify JSON format is valid

### API Cleanup Fails

1. Verify API endpoint is correct
2. Check authentication token
3. Ensure `requests` library is installed
4. Review API response status codes

## Commands Reference

```bash
# View registered jobs
cat test-results/test_jobs.json

# Clear job tracking
python cleanup.py --jobs

# Complete cleanup
python cleanup.py --all

# Cleanup old tracking entries (7+ days)
python -c "from utils.job_cleanup import JobCleanup; JobCleanup().clear_old_jobs(days=7)"
```

## Notes

- Job cleanup is **not automatic** by default
- Manual intervention may be required for failed cleanups
- Consider implementing cleanup in CI/CD pipelines
- Keep tracking file under version control (gitignored)
