# Multi-User Concurrent Testing Guide

## Overview

This guide shows how to test **multi-user concurrent flows** while keeping your main framework **synchronous**.

> **Note**: This guide was updated to use **Python threading** instead of async/await. The async approach had fundamental incompatibility issues with sync page objects. Threading provides true concurrent execution while keeping all your existing code unchanged!

### The Threading Approach (RECOMMENDED)

✅ **Keep**: Your existing sync framework (no changes needed!)
✅ **Add**: Python threading for multi-user scenarios
✅ **Benefit**: Simple threading + true concurrent execution
✅ **Works**: With all your existing sync page objects!

## Why This Approach?

### Problems with Full Async Conversion:
- ❌ Requires rewriting entire framework
- ❌ More complex code everywhere
- ❌ Harder to debug and maintain
- ❌ Steep learning curve for team
- ❌ Sync page objects incompatible with async playwright

### Threading Approach Benefits:
- ✅ **100% of code stays sync** (simple!)
- ✅ **Python threading** handles concurrency
- ✅ Reuse all existing page objects as-is
- ✅ Easy to understand and maintain
- ✅ True concurrent execution proven

## How It Works

### 1. Your Sync Code (Unchanged)
```python
# pom/login.py - stays exactly as is!
class LoginPage:
    def __init__(self, page):
        self.page = page

    def login(self, username, password):
        self.page.fill("#username", username)
        self.page.fill("#password", password)
        self.page.click("button[type='submit']")
        return FacilityPage(self.page)
```

### 2. Threading Wrapper (New)
```python
import threading
from playwright.sync_api import sync_playwright

# Regular sync function - no async needed!
def admin_workflow(results):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Import and use your SYNC page objects!
        from pom.login import LoginPage

        login_page = LoginPage(page)  # Sync object
        login_page.login(username, password)  # Sync method - works perfectly!

        results['admin'] = {"status": "success"}
```

### 3. Run Concurrently with Threading
```python
import threading

# Run multiple users at the same time
def test_multi_user():
    results = {}

    # Create threads for each user
    admin_thread = threading.Thread(target=admin_workflow, args=(results,))
    supervisor_thread = threading.Thread(target=supervisor_workflow, args=(results,))

    # Start BOTH at the SAME TIME!
    admin_thread.start()
    supervisor_thread.start()

    # Wait for both to complete
    admin_thread.join()
    supervisor_thread.join()

    print(results)  # Both users' results
```

## Real-World Example

See `tests/functional/test_multi_user_threading.py` for a complete working example:

```bash
# Run the multi-user concurrent test (Threading approach)
python tests/functional/test_multi_user_threading.py
```

### What You'll See:
1. **Two browser windows open simultaneously**
2. Facility Admin creating a job in window 1
3. Supervisor checking approvals in window 2
4. Both working at the same time (real concurrent behavior!)
5. Logs interleaved showing parallel actions

## Use Cases

### Perfect For:
✅ Testing concurrent parameter verification (admin fills, supervisor approves)
✅ Multiple users accessing same resource (race conditions)
✅ Real-time collaboration scenarios
✅ Load testing with multiple users

### Not Needed For:
❌ Single-user sequential tests (keep sync!)
❌ Simple CRUD operations
❌ Standard E2E tests

## Pattern for Your Tests

```python
import threading
from playwright.sync_api import sync_playwright

# 1. Define user workflows as regular sync functions
def user_a_workflow(results):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Use your SYNC page objects here - they work perfectly!
        from pom.login import LoginPage
        login_page = LoginPage(page)
        # ... your test logic
        results['user_a'] = {"status": "success"}

def user_b_workflow(results):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Use your SYNC page objects here!
        # ... your test logic
        results['user_b'] = {"status": "success"}

# 2. Run them concurrently with threading
def test_concurrent():
    results = {}

    # Create threads
    thread_a = threading.Thread(target=user_a_workflow, args=(results,))
    thread_b = threading.Thread(target=user_b_workflow, args=(results,))

    # Start both at once!
    thread_a.start()
    thread_b.start()

    # Wait for completion
    thread_a.join()
    thread_b.join()

    print(results)
```

## Tips

### Do's:
✅ Keep framework sync by default
✅ Use threading only for specific multi-user tests
✅ Each thread creates its own playwright instance
✅ Use threading.Thread() to run workflows concurrently
✅ Use shared results dictionary for communication

### Don'ts:
❌ Don't convert entire framework to async
❌ Don't use threading for single-user tests
❌ Don't share playwright instances between threads
❌ Don't over-engineer with threading everywhere

## Performance Comparison

### Sequential (Current Sync Approach):
```
Admin creates job:    30 seconds
Supervisor approves:  30 seconds
Total time:           60 seconds ⏱️
```

### Concurrent (Threading Approach):
```
Admin creates job:    30 seconds  ║
Supervisor approves:  30 seconds  ║ (runs at same time!)
Total time:           30 seconds ⏱️ (50% faster!)
```

## Summary

The **threading approach** gives you:
- ✅ True concurrent execution (for multi-user scenarios)
- ✅ Simplicity of sync (for 100% of your codebase!)
- ✅ No framework rewrite needed
- ✅ Easy to adopt incrementally
- ✅ Works with all existing page objects

**Bottom Line**: Keep it simple, use threading only where it truly adds value!
