# flake8: noqa E501
import json
import logging
from datetime import datetime

import pytest

from azure_datalake_logging.formatters.json_formatter import JsonFormatter


class TestJsonFormatter:
    """Test cases for the JsonFormatter class."""

    @pytest.fixture
    def formatter(self):
        """Create a formatter instance for testing."""
        return JsonFormatter()

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

    def test_initialization_with_defaults(self):
        """Test formatter initialization with default parameters."""
        # Arrange & Act
        formatter = JsonFormatter()

        # Assert
        assert formatter.sort_keys is True
        assert formatter.ensure_ascii is False
        assert formatter.indent is None
        assert formatter.default == str
        assert formatter.separators == (",", ":")

    def test_initialization_with_custom_parameters(self):
        """Test formatter initialization with custom parameters."""
        # Arrange & Act
        formatter = JsonFormatter(
            keys=["levelno", "process"],
            sort_keys=False,
            ensure_ascii=True,
            indent=2,
            default=repr,
            separators=(",", ": "),
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Assert
        assert formatter.sort_keys is False
        assert formatter.ensure_ascii is True
        assert formatter.indent == 2
        assert formatter.default == repr
        assert formatter.separators == (",", ": ")
        assert formatter.datefmt == "%Y-%m-%d %H:%M:%S"

    def test_format_method(self, formatter, log_record):
        """Test that format method returns valid JSON."""
        # Arrange

        # Act
        result = formatter.format(log_record)

        # Assert
        parsed = json.loads(result)
        assert parsed["name"] == "test_logger"
        assert parsed["levelname"] == "INFO"
        assert parsed["lineno"] == 10
        assert "created" in parsed
        assert parsed["message"] == "Test message"

    def test_format_with_timestamp_formatting(self, log_record):
        """Test JSON formatting with custom timestamp format."""
        # Arrange
        formatter = JsonFormatter(datefmt="%Y-%m-%d %H:%M:%S")
        timestamp = datetime.fromtimestamp(log_record.created).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Act
        result = formatter.format(log_record)

        # Assert
        parsed = json.loads(result)
        assert parsed["created"] == timestamp

    def test_format_with_custom_keys(self, log_record):
        """Test JSON formatting with custom keys."""
        # Arrange
        formatter = JsonFormatter(keys=["levelno", "process"])

        # Act
        result = formatter.format(log_record)

        # Assert
        parsed = json.loads(result)
        # Default keys should always be included
        assert "name" in parsed
        assert "levelname" in parsed
        assert "lineno" in parsed
        assert "created" in parsed
        # Custom keys should be included
        assert "levelno" in parsed
        assert "process" in parsed
        assert parsed["levelno"] == logging.INFO
        assert parsed["message"] == "Test message"

    def test_format_with_non_serializable_data(self):
        """Test handling of non-serializable data."""

        # Arrange
        class NonSerializable:
            pass

        entry = {
            "name": "test_logger",
            "level": logging.INFO,
            "pathname": "test_path.py",
            "lineno": 10,
            "msg": "Test with %s",
            "args": (NonSerializable(),),
            "exc_info": None,
        }

        formatter = JsonFormatter(keys=list(entry.keys()))
        record = logging.LogRecord(**entry)

        # Act & Assert
        with pytest.raises(TypeError) as excinfo:
            formatter.format(record)

        assert "Unable to serialize data to JSON format" in str(excinfo.value)
