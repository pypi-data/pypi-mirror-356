import logging as std_logging
import unittest
from io import StringIO
from logging import Formatter as StdFormatter

import azure_datalake_logging as test_logging


class TestLoggingCompatibility(unittest.TestCase):
    """Test compatibility with Python's standard logging module."""

    def setUp(self):
        """Set up test environment before each test."""
        # Reset logging configuration
        std_logging.root.handlers = []
        test_logging.root.handlers = []

        # Configure test logger
        self.log_stream = StringIO()
        self.handler = std_logging.StreamHandler(self.log_stream)
        self.test_logger = test_logging.getLogger("test_logger")
        self.test_logger.setLevel(test_logging.DEBUG)
        self.test_logger.addHandler(self.handler)

    def tearDown(self):
        """Clean up after each test."""
        self.log_stream.close()

    def test_import_alias(self):
        """Test that azure_datalake_logging can be imported as logging."""
        # Assert that modules have the same essential attributes
        test_attrs = set(dir(test_logging))

        # Check for critical logging attributes
        essential_attrs = [
            "Logger",
            "Handler",
            "Formatter",
            "Filter",
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
            "getLogger",
            "basicConfig",
            "exception",
        ]

        for attr in essential_attrs:
            self.assertIn(
                attr,
                test_attrs,
                f"Missing essential attribute: {attr}",
            )

    def test_log_levels(self):
        """Test that log levels are compatible."""
        self.assertEqual(std_logging.DEBUG, test_logging.DEBUG)
        self.assertEqual(std_logging.INFO, test_logging.INFO)
        self.assertEqual(std_logging.WARNING, test_logging.WARNING)
        self.assertEqual(std_logging.ERROR, test_logging.ERROR)
        self.assertEqual(std_logging.CRITICAL, test_logging.CRITICAL)

    def test_basic_logging_functions(self):
        """Test that basic logging functions work correctly."""
        test_logging.basicConfig(level=test_logging.DEBUG)

        self.test_logger.debug("Debug message")
        self.test_logger.info("Info message")
        self.test_logger.warning("Warning message")
        self.test_logger.error("Error message")
        self.test_logger.critical("Critical message")

        log_output = self.log_stream.getvalue()

        self.assertIn("Debug message", log_output)
        self.assertIn("Info message", log_output)
        self.assertIn("Warning message", log_output)
        self.assertIn("Error message", log_output)
        self.assertIn("Critical message", log_output)

    def test_filter_compatibility(self):
        """Test that filters are compatible."""

        class TestFilter(std_logging.Filter):
            def filter(self, record):
                return "allow" in record.getMessage().lower()

        test_filter = TestFilter()
        self.test_logger.addFilter(test_filter)

        self.test_logger.info("This message is allowed")
        self.test_logger.info("This message is blocked")

        log_output = self.log_stream.getvalue()
        self.assertIn("allowed", log_output)
        self.assertNotIn("blocked", log_output)

    def test_exception_logging(self):
        """Test exception logging compatibility."""
        try:
            msg = "Test exception"
            raise ValueError(msg)
        except ValueError:
            self.test_logger.exception("An exception occurred")

        log_output = self.log_stream.getvalue()
        self.assertIn("An exception occurred", log_output)
        self.assertIn("ValueError: Test exception", log_output)
        self.assertIn("Traceback", log_output)


class TestConfigurationCompatibility(unittest.TestCase):
    """Test logging configuration compatibility."""

    def setUp(self):
        """Set up test environment."""
        # Reset logging configuration
        std_logging.root.handlers = []
        test_logging.root.handlers = []

    def test_basic_config(self):
        """Test basicConfig functionality."""
        # Configure with basicConfig
        test_logging.basicConfig(
            level=test_logging.INFO,
            format="%(levelname)s - %(message)s",
        )

        # Check if root logger is configured correctly
        self.assertEqual(test_logging.root.level, test_logging.INFO)
        self.assertGreaterEqual(len(test_logging.root.handlers), 1)

        # Get a logger and test logging
        # logger = test_logging.getLogger("basic_config_test")
        stream_handler = None

        # Find StreamHandler in root handlers
        for handler in test_logging.root.handlers:
            if isinstance(handler, test_logging.StreamHandler):
                stream_handler = handler
                break

        self.assertIsNotNone(
            stream_handler,
            "StreamHandler not found in root handlers",
        )

        if stream_handler:
            formatter = stream_handler.formatter
            self.assertIsNotNone(formatter)

            # Test formatting
            record = test_logging.LogRecord(
                "test",
                test_logging.INFO,
                "",
                0,
                "Test message",
                (),
                None,
            )
            formatted = formatter.format(record)
            self.assertEqual("INFO - Test message", formatted)


if __name__ == "__main__":
    unittest.main()
