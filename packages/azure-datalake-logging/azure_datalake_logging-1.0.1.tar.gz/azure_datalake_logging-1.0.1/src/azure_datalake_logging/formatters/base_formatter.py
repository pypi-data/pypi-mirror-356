# flake8: noqa E501

from abc import ABC, abstractmethod
from logging import Formatter, LogRecord
from typing import Any


class BaseFormatter(Formatter, ABC):
    """
    Abstract base class for all formatters in the azure_datalake_logging package.

    This class extends the standard logging.Formatter
    and defines the interface that all custom formatters must implement.
    """

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: str = "%",
        validate: bool = True,
    ) -> None:
        """
        Initialize the formatter with specified format strings.

        Args:
            fmt: The format string for the message
            datefmt: The format string for the date/time portion of the log record
            style: The style of the format string (%, {, or $)
            validate: Whether to validate the format string
        """
        super().__init__(fmt, datefmt, style, validate)

    @abstractmethod
    def format(self, record: LogRecord) -> str:
        """
        Format the specified record as text.

        This abstract method must be implemented by subclasses
        to define how log records are formatted.

        Args:
            record: The log record to format

        Returns:
            The formatted log message as a string
        """
        msg = "Subclasses must implement format()"
        raise NotImplementedError(msg)

    def enrich_log_record(self, record: LogRecord) -> LogRecord:
        """
        Enrich the log record with additional context or metadata.

        Args:
            record: The log record to enrich

        Returns:
            The enriched log record
        """
        return record

    def to_dict(self, record: LogRecord) -> dict[str, Any]:
        """
        Convert a log record to a dictionary representation.

        Args:
            record: The log record to convert

        Returns:
            Dictionary representation of the log record with standard fields
        """
        return {
            "level": record.levelname,
            "logger": record.name,
            "timestamp": self.formatTime(record),
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
            "process": record.process,
            "thread": record.thread,
        }
