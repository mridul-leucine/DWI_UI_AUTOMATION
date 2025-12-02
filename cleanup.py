"""
Cleanup script for test artifacts and generated data.
Run this after tests to clean up screenshots, logs, and test data.
"""

import os
import shutil
import json
from pathlib import Path


def cleanup_screenshots(days=7):
    """Remove screenshots older than specified days."""
    print("Cleaning up screenshots...")
    screenshot_dir = "test-results/screenshots"

    if os.path.exists(screenshot_dir):
        import time
        cutoff_time = time.time() - (days * 86400)

        count = 0
        for filename in os.listdir(screenshot_dir):
            file_path = os.path.join(screenshot_dir, filename)

            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)

                if file_time < cutoff_time:
                    os.remove(file_path)
                    count += 1

        print(f"✓ Removed {count} old screenshots")
    else:
        print("✓ No screenshots directory found")


def cleanup_logs(days=30):
    """Remove logs older than specified days."""
    print("Cleaning up logs...")
    log_dir = "test-results/logs"

    if os.path.exists(log_dir):
        import time
        cutoff_time = time.time() - (days * 86400)

        count = 0
        for filename in os.listdir(log_dir):
            file_path = os.path.join(log_dir, filename)

            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)

                if file_time < cutoff_time:
                    os.remove(file_path)
                    count += 1

        print(f"✓ Removed {count} old log files")
    else:
        print("✓ No logs directory found")


def cleanup_videos():
    """Remove all test execution videos."""
    print("Cleaning up videos...")
    video_dir = "test-results/videos"

    if os.path.exists(video_dir):
        try:
            shutil.rmtree(video_dir)
            print("✓ Removed all videos")
        except Exception as e:
            print(f"✗ Failed to remove videos: {str(e)}")
    else:
        print("✓ No videos directory found")


def cleanup_pytest_cache():
    """Remove pytest cache."""
    print("Cleaning up pytest cache...")

    cache_dirs = [".pytest_cache", "tests/.pytest_cache", "tests/functional/.pytest_cache"]

    count = 0
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                count += 1
            except Exception as e:
                print(f"✗ Failed to remove {cache_dir}: {str(e)}")

    if count > 0:
        print(f"✓ Removed {count} pytest cache directories")
    else:
        print("✓ No pytest cache found")


def cleanup_pycache():
    """Remove Python cache files."""
    print("Cleaning up Python cache...")

    count = 0
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                count += 1
            except Exception as e:
                print(f"✗ Failed to remove {pycache_path}: {str(e)}")

    if count > 0:
        print(f"✓ Removed {count} __pycache__ directories")
    else:
        print("✓ No __pycache__ found")


def cleanup_test_jobs_tracking():
    """Remove test jobs tracking file."""
    print("Cleaning up test jobs tracking...")

    jobs_file = "test-results/test_jobs.json"

    if os.path.exists(jobs_file):
        try:
            with open(jobs_file, 'r') as f:
                data = json.load(f)

            job_count = len(data.get("jobs", []))

            if job_count > 0:
                print(f"⚠ Warning: {job_count} test jobs are tracked but not cleaned up")
                print("  Consider running job cleanup before removing tracking file")
                print("  Use: python -m utils.job_cleanup")

            # Clear the tracking file
            with open(jobs_file, 'w') as f:
                json.dump({"jobs": []}, f, indent=2)

            print("✓ Cleared test jobs tracking file")
        except Exception as e:
            print(f"✗ Failed to cleanup jobs tracking: {str(e)}")
    else:
        print("✓ No test jobs tracking file found")


def cleanup_all():
    """Run all cleanup tasks."""
    print("\n" + "="*60)
    print("Starting cleanup...")
    print("="*60 + "\n")

    cleanup_screenshots(days=7)
    cleanup_logs(days=30)
    cleanup_videos()
    cleanup_test_jobs_tracking()
    cleanup_pytest_cache()
    cleanup_pycache()

    print("\n" + "="*60)
    print("Cleanup completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cleanup test artifacts")
    parser.add_argument("--screenshots", action="store_true", help="Clean up screenshots")
    parser.add_argument("--logs", action="store_true", help="Clean up logs")
    parser.add_argument("--videos", action="store_true", help="Clean up videos")
    parser.add_argument("--cache", action="store_true", help="Clean up pytest cache")
    parser.add_argument("--pycache", action="store_true", help="Clean up Python cache")
    parser.add_argument("--jobs", action="store_true", help="Clean up test jobs tracking")
    parser.add_argument("--all", action="store_true", help="Clean up everything")
    parser.add_argument("--days", type=int, default=7, help="Days to keep screenshots (default: 7)")

    args = parser.parse_args()

    if args.all or not any([args.screenshots, args.logs, args.videos, args.cache, args.pycache, args.jobs]):
        cleanup_all()
    else:
        print("\n" + "="*60)
        print("Starting selective cleanup...")
        print("="*60 + "\n")

        if args.screenshots:
            cleanup_screenshots(args.days)

        if args.logs:
            cleanup_logs(30)

        if args.videos:
            cleanup_videos()

        if args.jobs:
            cleanup_test_jobs_tracking()

        if args.cache:
            cleanup_pytest_cache()

        if args.pycache:
            cleanup_pycache()

        print("\n" + "="*60)
        print("Cleanup completed!")
        print("="*60 + "\n")
