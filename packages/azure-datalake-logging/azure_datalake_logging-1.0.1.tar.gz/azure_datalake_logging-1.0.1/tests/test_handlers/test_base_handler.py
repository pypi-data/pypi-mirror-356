import logging
from unittest.mock import Mock

import pytest

from azure_datalake_logging.handlers.base_handler import BaseHandler


class ConcreteHandler(BaseHandler):
    """Concrete implementation of BaseHandler for testing."""

    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.emitted_records = []

    def emit(self, record):
        """Test implementation that simply stores the record."""
        self.emitted_records.append(record)


class TestBaseHandler:
    """Test cases for the BaseHandler class."""

    @pytest.fixture
    def handler(self):
        """Create a concrete handler instance for testing."""
        return ConcreteHandler(level=logging.INFO)

    @pytest.fixture
    def log_record(self):
        """Create a sample log record for testing."""
        return logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test_path.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

    def test_initialization(self, handler):
        """Test that handler initializes with correct level."""
        assert handler.level == logging.INFO
        assert isinstance(handler.formatter, type(None))

    def test_handle_method(self, handler, log_record):
        """Test that handle method processes records correctly."""
        # Arrange
        # Act
        result = handler.handle(log_record)

        # Assert
        assert result is True
        assert len(handler.emitted_records) == 1
        assert handler.emitted_records[0] == log_record

    def test_setlevel_method(self, handler):
        """Test setting the handler's log level."""
        # Arrange
        # Act
        handler.setLevel(logging.DEBUG)

        # Assert
        assert handler.level == logging.DEBUG

    def test_set_formatter(self, handler):
        """Test setting a formatter for the handler."""
        # Arrange
        formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

        # Act
        handler.setFormatter(formatter)

        # Assert
        assert handler.formatter == formatter

    def test_format_method(self, handler, log_record):
        """Test that format method uses formatter if set."""
        # Arrange
        formatter = Mock()
        formatter.format.return_value = "Formatted message"
        handler.setFormatter(formatter)

        # Act
        result = handler.format(log_record)

        # Assert
        formatter.format.assert_called_once_with(log_record)
        assert result == "Formatted message"

    def test_format_method_no_formatter(self, handler, log_record):
        """Test that format method returns message when no formatter is set."""
        # Act
        result = handler.format(log_record)

        # Assert
        assert result == log_record.getMessage()

    def test_filter_method(self, handler, log_record):
        """Test that filter method applies filters correctly."""
        # Arrange
        test_filter = Mock()
        test_filter.filter.return_value = False
        handler.addFilter(test_filter)

        # Act
        result = handler.filter(log_record)

        # Assert
        test_filter.filter.assert_called_once_with(log_record)
        assert result is False
