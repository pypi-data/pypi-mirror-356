import logging as std_logging
import os
import tempfile
import unittest

import azure_datalake_logging as test_logging


class TestLoggingReplacement(unittest.TestCase):
    """
    Test real-world usage of azure_datalake_logging
    as a replacement for logging.
    """

    def setUp(self):
        """Set up test environment."""
        # Reset logging configuration
        std_logging.root.handlers = []
        test_logging.root.handlers = []

        # Create temp file for logging
        self.log_fd, self.log_path = tempfile.mkstemp()

    def tearDown(self):
        """Clean up after each test."""
        os.close(self.log_fd)
        if os.path.exists(self.log_path):
            os.unlink(self.log_path)

    def test_file_logging_workflow(self):
        """Test a complete file logging workflow."""
        # Configure logging to file
        test_logging.basicConfig(
            level=test_logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename=self.log_path,
            filemode="w",
        )

        # Create logger
        logger = test_logging.getLogger("workflow_test")

        # Log different message types
        logger.debug("Debug information")
        logger.info("Information message")
        logger.warning("Warning message")
        logger.error("Error occurred")

        # Add a custom handler for in-memory logging
        memory_output = []

        class MemoryHandler(test_logging.Handler):
            def emit(self, record):
                memory_output.append(self.format(record))

        memory_handler = MemoryHandler()
        memory_handler.setLevel(test_logging.WARNING)
        memory_handler.setFormatter(
            test_logging.Formatter("MEMORY: %(levelname)s - %(message)s"),
        )
        logger.addHandler(memory_handler)

        # More logging with both handlers
        logger.debug("Another debug")
        logger.info("Another info")
        logger.warning("Another warning")
        logger.error("Another error")

        # Check file output
        with open(self.log_path) as log_file:
            log_content = log_file.read()

        # Verify all log levels are in file
        self.assertIn("Debug information", log_content)
        self.assertIn("Information message", log_content)
        self.assertIn("Warning message", log_content)
        self.assertIn("Error occurred", log_content)
        self.assertIn("Another debug", log_content)
        self.assertIn("Another info", log_content)
        self.assertIn("Another warning", log_content)
        self.assertIn("Another error", log_content)

        # Verify memory handler only received warnings and errors
        self.assertEqual(2, len(memory_output))
        self.assertIn("MEMORY: WARNING - Another warning", memory_output)
        self.assertIn("MEMORY: ERROR - Another error", memory_output)


if __name__ == "__main__":
    unittest.main()
