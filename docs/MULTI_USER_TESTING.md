# Multi-User Concurrent Testing Guide

## Overview

This guide shows how to test **multi-user concurrent flows** while keeping your main framework **synchronous**.

### The Hybrid Approach

✅ **Keep**: Your existing sync framework (no changes needed!)
✅ **Add**: Async wrappers only for multi-user scenarios
✅ **Benefit**: Best of both worlds - simple code + concurrent execution

## Why This Approach?

### Problems with Full Async Conversion:
- ❌ Requires rewriting entire framework
- ❌ More complex code everywhere
- ❌ Harder to debug and maintain
- ❌ Steep learning curve for team

### Hybrid Approach Benefits:
- ✅ **90% of code stays sync** (simple!)
- ✅ **10% async wrappers** for multi-user scenarios
- ✅ Reuse all existing page objects
- ✅ Easy to understand and maintain

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

### 2. Async Wrapper (New)
```python
# Wrap sync code in async function
async def admin_workflow(browser_context):
    page = await browser_context.new_page()

    # Import and use your SYNC page objects!
    from pom.login import LoginPage

    login_page = LoginPage(page)  # Sync object
    login_page.login(username, password)  # Sync method

    await page.wait_for_timeout(1000)  # Just add await for page operations
```

### 3. Run Concurrently
```python
# Run multiple users at the same time
async def test_multi_user():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # Two separate contexts (isolated sessions)
        admin_context = await browser.new_context()
        supervisor_context = await browser.new_context()

        # Run BOTH at the SAME TIME!
        admin_result, supervisor_result = await asyncio.gather(
            admin_workflow(admin_context),
            supervisor_workflow(supervisor_context)
        )
```

## Real-World Example

See `tests/functional/test_multi_user_concurrent.py` for a complete example:

```bash
# Run the multi-user concurrent test
python tests/functional/test_multi_user_concurrent.py
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
# 1. Define user workflows as async functions
async def user_a_workflow(context):
    page = await context.new_page()
    # Use your SYNC page objects here!
    # Just add await for page operations
    pass

async def user_b_workflow(context):
    page = await context.new_page()
    # Use your SYNC page objects here!
    pass

# 2. Run them concurrently
async def test_concurrent():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx_a = await browser.new_context()
        ctx_b = await browser.new_context()

        # Run both at once!
        result_a, result_b = await asyncio.gather(
            user_a_workflow(ctx_a),
            user_b_workflow(ctx_b)
        )
```

## Tips

### Do's:
✅ Keep framework sync by default
✅ Add async only for specific multi-user tests
✅ Use separate browser contexts for each user
✅ Use asyncio.gather() to run workflows concurrently

### Don'ts:
❌ Don't convert entire framework to async
❌ Don't use async for single-user tests
❌ Don't share pages between users
❌ Don't over-engineer with async everywhere

## Performance Comparison

### Sequential (Current Sync Approach):
```
Admin creates job:    30 seconds
Supervisor approves:  30 seconds
Total time:           60 seconds ⏱️
```

### Concurrent (Hybrid Approach):
```
Admin creates job:    30 seconds  ║
Supervisor approves:  30 seconds  ║ (runs at same time!)
Total time:           30 seconds ⏱️ (50% faster!)
```

## Summary

The **hybrid sync/async approach** gives you:
- ✅ Speed benefits of async (for multi-user scenarios)
- ✅ Simplicity of sync (for 90% of your tests)
- ✅ No framework rewrite needed
- ✅ Easy to adopt incrementally

**Bottom Line**: Keep it simple, add async only where it truly adds value!
