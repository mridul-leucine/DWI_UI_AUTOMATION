"""
Test Data Manager utility for loading and managing test data.
"""

import json
import os
from datetime import datetime


class TestDataManager:
    """
    Utility class for managing test data from JSON files.
    """

    def __init__(self, data_dir="data"):
        """
        Initialize TestDataManager.

        Args:
            data_dir: Directory containing test data files
        """
        self.data_dir = data_dir
        self._credentials = None
        self._test_data = None
        self._config = None

    def get_credentials(self):
        """
        Load and return user credentials.

        Returns:
            dict: Credentials dictionary with username and password
        """
        if self._credentials is None:
            self._credentials = self._load_json_file("credentials.json")
        return self._credentials

    def get_test_data(self, process_name="qa_ui_all_para"):
        """
        Load and return test data for a specific process.

        Args:
            process_name: Name of the process (default: qa_ui_all_para)

        Returns:
            dict: Test data dictionary
        """
        if self._test_data is None:
            filename = f"{process_name}_test_data.json"
            self._test_data = self._load_json_file(filename)
        return self._test_data

    def get_config(self):
        """
        Load and return configuration settings.

        Returns:
            dict: Configuration dictionary
        """
        if self._config is None:
            self._config = self._load_json_file("config.json")
        return self._config

    def get_parameter_value(self, parameter_name):
        """
        Get value for a specific parameter.

        Args:
            parameter_name: Name of the parameter

        Returns:
            str/int: Parameter value
        """
        test_data = self.get_test_data()
        parameters = test_data.get("parameters", {})
        return parameters.get(parameter_name)

    def get_test_image_path(self):
        """
        Get the path to the test image file.

        Returns:
            str: Absolute path to test image
        """
        test_data = self.get_test_data()
        relative_path = test_data.get("parameters", {}).get("Image", "test-resources/images/sample-test-image.jpg")

        # Convert to absolute path
        abs_path = os.path.abspath(relative_path)
        return abs_path

    def generate_random_job_code(self, prefix="TEST"):
        """
        Generate a random job code for testing.

        Args:
            prefix: Prefix for the job code

        Returns:
            str: Generated job code
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}-{timestamp}"

    def get_base_url(self):
        """
        Get the base URL from configuration.

        Returns:
            str: Base URL
        """
        config = self.get_config()
        return config.get("baseUrl", "https://qa.platform.leucinetech.com")

    def get_timeout(self, timeout_type="default"):
        """
        Get timeout value from configuration.

        Args:
            timeout_type: Type of timeout (default, navigation, element)

        Returns:
            int: Timeout in milliseconds
        """
        config = self.get_config()
        timeouts = config.get("timeout", {})
        return timeouts.get(timeout_type, 30000)

    def get_browser_config(self):
        """
        Get browser configuration settings.

        Returns:
            dict: Browser configuration
        """
        config = self.get_config()
        return config.get("browser", {})

    def _load_json_file(self, filename):
        """
        Load a JSON file from the data directory.

        Args:
            filename: Name of the JSON file

        Returns:
            dict: Parsed JSON data
        """
        file_path = os.path.join(self.data_dir, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Test data file not found: {file_path}")

        with open(file_path, 'r') as f:
            return json.load(f)

    def reload_data(self):
        """
        Reload all cached data (useful for test teardown/setup).
        """
        self._credentials = None
        self._test_data = None
        self._config = None


# Singleton instance
_test_data_manager = TestDataManager()


def get_test_data_manager():
    """
    Get the singleton TestDataManager instance.

    Returns:
        TestDataManager: Singleton instance
    """
    return _test_data_manager
