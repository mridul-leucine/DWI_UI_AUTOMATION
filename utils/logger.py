"""
Logger utility for test execution logging.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class TestLogger:
    """
    Utility class for logging test execution details.
    """

    def __init__(self, log_dir="test-results/logs", log_level=logging.DEBUG):
        """
        Initialize TestLogger.

        Args:
            log_dir: Directory to save log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = log_dir
        self.log_level = log_level

        # Create log directory if it doesn't exist
        Path(log_dir).mkdir(parents=True, exist_ok=True)

        # Initialize logger
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """
        Setup and configure the logger.

        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logger
        logger = logging.getLogger("DWI_Automation")
        logger.setLevel(self.log_level)

        # Clear any existing handlers
        logger.handlers.clear()

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

        # File handler for detailed logs
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.log_dir, f"test_execution_{timestamp}.log")

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)

        # Console handler for simple logs
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.info(f"Logger initialized. Log file: {log_file}")

        return logger

    def debug(self, message, **kwargs):
        """Log debug message."""
        self.logger.debug(message, extra=kwargs)

    def info(self, message, **kwargs):
        """Log info message."""
        self.logger.info(message, extra=kwargs)

    def warning(self, message, **kwargs):
        """Log warning message."""
        self.logger.warning(message, extra=kwargs)

    def error(self, message, exception=None, **kwargs):
        """
        Log error message.

        Args:
            message: Error message
            exception: Exception object (optional)
        """
        if exception:
            self.logger.error(f"{message} - Exception: {str(exception)}", exc_info=True, extra=kwargs)
        else:
            self.logger.error(message, extra=kwargs)

    def critical(self, message, **kwargs):
        """Log critical message."""
        self.logger.critical(message, extra=kwargs)

    def log_test_start(self, test_name):
        """
        Log the start of a test.

        Args:
            test_name: Name of the test
        """
        self.info("=" * 80)
        self.info(f"TEST START: {test_name}")
        self.info("=" * 80)

    def log_test_end(self, test_name, status="PASSED"):
        """
        Log the end of a test.

        Args:
            test_name: Name of the test
            status: Test status (PASSED, FAILED, SKIPPED)
        """
        self.info("-" * 80)
        self.info(f"TEST END: {test_name} - Status: {status}")
        self.info("=" * 80)

    def log_step(self, step_number, step_description):
        """
        Log a test step.

        Args:
            step_number: Step number
            step_description: Description of the step
        """
        self.info(f"[Step {step_number}] {step_description}")

    def log_action(self, action, element="", value=""):
        """
        Log a test action.

        Args:
            action: Action being performed (e.g., 'click', 'type', 'select')
            element: Element being acted upon
            value: Value being used (for type/select actions)
        """
        message = f"Action: {action}"
        if element:
            message += f" on '{element}'"
        if value:
            message += f" with value '{value}'"

        self.debug(message)

    def log_verification(self, description, result):
        """
        Log a verification result.

        Args:
            description: Description of what was verified
            result: Verification result (True/False)
        """
        status = "PASS" if result else "FAIL"
        message = f"Verification [{status}]: {description}"

        if result:
            self.info(message)
        else:
            self.error(message)

    def log_parameter_fill(self, parameter_name, parameter_value):
        """
        Log parameter filling action.

        Args:
            parameter_name: Name of the parameter
            parameter_value: Value being filled
        """
        self.info(f"Filling parameter '{parameter_name}' with value: {parameter_value}")

    def cleanup_old_logs(self, days=30):
        """
        Clean up log files older than specified days.

        Args:
            days: Number of days to keep logs
        """
        try:
            import time

            cutoff_time = time.time() - (days * 86400)

            for filename in os.listdir(self.log_dir):
                if filename.endswith('.log'):
                    file_path = os.path.join(self.log_dir, filename)

                    if os.path.isfile(file_path):
                        file_time = os.path.getmtime(file_path)

                        if file_time < cutoff_time:
                            os.remove(file_path)
                            print(f"Removed old log: {filename}")

        except Exception as e:
            print(f"Failed to cleanup old logs: {str(e)}")


# Global logger instance
_test_logger = None


def get_logger():
    """
    Get the global TestLogger instance.

    Returns:
        TestLogger: Global logger instance
    """
    global _test_logger

    if _test_logger is None:
        _test_logger = TestLogger()

    return _test_logger
