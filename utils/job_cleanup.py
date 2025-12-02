"""
Job Cleanup utility for removing test jobs after test execution.
Supports UI-based, API-based, and database cleanup strategies.
"""

import json
import os
from datetime import datetime
from pathlib import Path


class JobCleanup:
    """
    Utility class for cleaning up test jobs created during test execution.
    """

    def __init__(self, page=None, cleanup_strategy="ui"):
        """
        Initialize JobCleanup.

        Args:
            page: Playwright page object (required for UI-based cleanup)
            cleanup_strategy: Cleanup strategy ('ui', 'api', 'database')
        """
        self.page = page
        self.cleanup_strategy = cleanup_strategy
        self.jobs_file = "test-results/test_jobs.json"
        self._ensure_jobs_file_exists()

    def _ensure_jobs_file_exists(self):
        """Ensure the jobs tracking file exists."""
        Path("test-results").mkdir(parents=True, exist_ok=True)

        if not os.path.exists(self.jobs_file):
            with open(self.jobs_file, 'w') as f:
                json.dump({"jobs": []}, f, indent=2)

    def register_job(self, job_code, test_name, additional_info=None):
        """
        Register a test job for cleanup.

        Args:
            job_code: Job code/ID
            test_name: Name of the test that created the job
            additional_info: Additional information about the job
        """
        try:
            with open(self.jobs_file, 'r') as f:
                data = json.load(f)

            job_entry = {
                "job_code": job_code,
                "test_name": test_name,
                "created_at": datetime.now().isoformat(),
                "additional_info": additional_info or {}
            }

            data["jobs"].append(job_entry)

            with open(self.jobs_file, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"✓ Registered job for cleanup: {job_code}")

        except Exception as e:
            print(f"✗ Failed to register job: {str(e)}")

    def cleanup_job_via_ui(self, job_code):
        """
        Clean up a job using UI navigation.

        Args:
            job_code: Job code to clean up

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.page:
            print("✗ Page object not provided for UI cleanup")
            return False

        try:
            print(f"Attempting UI cleanup for job: {job_code}")

            # Navigate to jobs list page (adjust URL as needed)
            self.page.goto(f"{self.page.url.split('/job/')[0]}/jobs")
            self.page.wait_for_timeout(2000)

            # Search for the job
            search_input = self.page.locator("input[placeholder*='Search'], input[type='search']").first
            if search_input.count() > 0:
                search_input.fill(job_code)
                self.page.wait_for_timeout(1000)

            # Look for delete/archive button
            # This is a generic approach - adjust selectors based on actual UI
            delete_selectors = [
                f"button[aria-label*='delete']:near(text='{job_code}')",
                f"button:has-text('Delete'):near(text='{job_code}')",
                f"button:has-text('Remove'):near(text='{job_code}')",
                f"[data-testid='delete-job-{job_code}']",
                f"button.delete-button:near(text='{job_code}')"
            ]

            deleted = False
            for selector in delete_selectors:
                delete_button = self.page.locator(selector).first
                if delete_button.count() > 0:
                    delete_button.click()
                    self.page.wait_for_timeout(500)

                    # Confirm deletion if confirmation dialog appears
                    confirm_button = self.page.locator(
                        "button:has-text('Confirm'), button:has-text('Yes'), button:has-text('Delete')"
                    ).first
                    if confirm_button.count() > 0:
                        confirm_button.click()
                        self.page.wait_for_timeout(1000)

                    deleted = True
                    print(f"✓ Deleted job via UI: {job_code}")
                    break

            if not deleted:
                print(f"⚠ Could not find delete button for job: {job_code}")
                return False

            return True

        except Exception as e:
            print(f"✗ Failed to cleanup job via UI: {str(e)}")
            return False

    def cleanup_job_via_api(self, job_code, base_url, auth_token=None):
        """
        Clean up a job using API.

        Args:
            job_code: Job code to clean up
            base_url: API base URL
            auth_token: Authentication token

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import requests

            headers = {}
            if auth_token:
                headers["Authorization"] = f"Bearer {auth_token}"

            # Attempt to delete via API (adjust endpoint as needed)
            response = requests.delete(
                f"{base_url}/api/jobs/{job_code}",
                headers=headers,
                timeout=10
            )

            if response.status_code in [200, 204]:
                print(f"✓ Deleted job via API: {job_code}")
                return True
            else:
                print(f"⚠ API cleanup failed with status {response.status_code}")
                return False

        except ImportError:
            print("✗ 'requests' library not installed. Cannot use API cleanup.")
            return False
        except Exception as e:
            print(f"✗ Failed to cleanup job via API: {str(e)}")
            return False

    def cleanup_all_registered_jobs(self):
        """
        Clean up all registered test jobs.

        Returns:
            dict: Summary of cleanup results
        """
        try:
            with open(self.jobs_file, 'r') as f:
                data = json.load(f)

            jobs = data.get("jobs", [])

            if not jobs:
                print("✓ No jobs to clean up")
                return {"total": 0, "success": 0, "failed": 0}

            print(f"\nCleaning up {len(jobs)} test jobs...")

            results = {"total": len(jobs), "success": 0, "failed": 0}

            for job in jobs:
                job_code = job["job_code"]

                if self.cleanup_strategy == "ui":
                    success = self.cleanup_job_via_ui(job_code)
                elif self.cleanup_strategy == "api":
                    # API cleanup requires additional parameters
                    print(f"⚠ API cleanup not fully configured for {job_code}")
                    success = False
                else:
                    print(f"⚠ Unsupported cleanup strategy: {self.cleanup_strategy}")
                    success = False

                if success:
                    results["success"] += 1
                else:
                    results["failed"] += 1

            # Clear the jobs file after cleanup
            with open(self.jobs_file, 'w') as f:
                json.dump({"jobs": []}, f, indent=2)

            print(f"\nCleanup Summary:")
            print(f"  Total jobs: {results['total']}")
            print(f"  Successfully cleaned: {results['success']}")
            print(f"  Failed: {results['failed']}")

            return results

        except Exception as e:
            print(f"✗ Failed to cleanup registered jobs: {str(e)}")
            return {"total": 0, "success": 0, "failed": 0}

    def get_registered_jobs(self):
        """
        Get list of all registered jobs.

        Returns:
            list: List of registered jobs
        """
        try:
            with open(self.jobs_file, 'r') as f:
                data = json.load(f)
            return data.get("jobs", [])
        except Exception as e:
            print(f"✗ Failed to get registered jobs: {str(e)}")
            return []

    def clear_old_jobs(self, days=7):
        """
        Remove jobs older than specified days from tracking file.

        Args:
            days: Number of days to keep jobs
        """
        try:
            from datetime import timedelta

            with open(self.jobs_file, 'r') as f:
                data = json.load(f)

            jobs = data.get("jobs", [])
            cutoff_date = datetime.now() - timedelta(days=days)

            filtered_jobs = []
            removed_count = 0

            for job in jobs:
                try:
                    created_at = datetime.fromisoformat(job["created_at"])
                    if created_at > cutoff_date:
                        filtered_jobs.append(job)
                    else:
                        removed_count += 1
                except:
                    # Keep jobs with invalid dates
                    filtered_jobs.append(job)

            data["jobs"] = filtered_jobs

            with open(self.jobs_file, 'w') as f:
                json.dump(data, f, indent=2)

            if removed_count > 0:
                print(f"✓ Removed {removed_count} old job entries from tracking")

        except Exception as e:
            print(f"✗ Failed to clear old jobs: {str(e)}")


# Convenience function for pytest fixtures
def cleanup_test_jobs(page):
    """
    Convenience function to cleanup all test jobs.
    Use this in pytest teardown.

    Args:
        page: Playwright page object
    """
    cleanup = JobCleanup(page, cleanup_strategy="ui")
    cleanup.cleanup_all_registered_jobs()
