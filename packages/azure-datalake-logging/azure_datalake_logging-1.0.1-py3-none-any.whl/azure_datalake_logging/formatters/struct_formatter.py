from datetime import datetime
from enum import Enum
from logging import LogRecord
from typing import Any

from .base_formatter import BaseFormatter


class DefaultKeys(Enum):
    name = "name"
    levelname = "levelname"
    lineno = "lineno"
    created = "created"


class ExtendedKeys(Enum):
    args = "args"
    levelno = "levelno"
    pathname = "pathname"
    exc_info = "exc_info"
    exc_text = "exc_text"
    stack_info = "stack_info"
    msecs = "msecs"
    relativeCreated = "relativeCreated"
    thread = "thread"
    threadName = "threadName"
    processName = "processName"
    process = "process"


DEFAULT_KEYS = set(DefaultKeys.__members__.keys())
DEFAULT_VALUES = {DefaultKeys[key].value for key in DEFAULT_KEYS}

EXTENDED_KEYS = set(ExtendedKeys.__members__.keys())
EXTENDED_VALUES = {ExtendedKeys[key].value for key in EXTENDED_KEYS}


class StructFormatter(BaseFormatter):
    """
    Formats input data as a JSON string.

    This formatter converts Python dictionaries or other serializable
    objects into valid JSON strings.
    """

    def __init__(
        self,
        keys: str | list[str] | set[str] = None,
        datefmt: str = None,
        fmt: str = None,
    ) -> None:
        """
        Initialize the JSON formatter with optional formatting parameters.

        Args:
            keys:
                List or set of log record attributes to include in output.
                If None, default keys will be used.
                sort_keys: Whether to sort dictionary keys in JSON output.

            datefmt:
                Format string for the created timestamp. If provided,
                converts the timestamp to formatted string.

        Note:
            The formatter always includes default keys (name, levelname,
            lineno, created) and the log message.
        """
        super().__init__(fmt, datefmt)
        self.keys = self._set_keys(keys)
        self.datefmt = datefmt

    def _set_keys(
        self,
        keys: str | list[str] | set[str] | None = None,
    ) -> set[str]:
        """
        Process and validate the input keys, returning a set of valid keys.
        This method handles different input types (string, list, set, or None)
        and ensures that only valid keys from ExtendedKeys enum are included in
        the result, combined with the default keys.

        Args:
            keys: Input keys that can be:
                - None: Returns DEFAULT_VALUES
                - str: Single key or comma-separated keys
                - list[str]: List of keys
                - set[str]: Set of keys

        Returns:
            set (str): A set containing the default keys
            plus any valid additional keys

        """
        if not bool(keys):
            return DEFAULT_VALUES

        if isinstance(keys, str):
            if "," in keys:
                keys = [key.strip() for key in keys.split(",")]
            else:
                keys = [keys]

        extended_keys = set(ExtendedKeys.__members__.keys())

        return DEFAULT_KEYS | {key for key in keys if key in extended_keys}

    def _create_record(self, data: LogRecord) -> dict[str, Any]:
        """
        Creates a dictionary record from a LogRecord object.

        This method extracts the specified keys from the LogRecord object
        and adds the formatted message to create a complete record
        for JSON serialization.

        Args:
            data (LogRecord): The log record to convert into a dictionary.

        Returns:
            dict (str, Any): A dictionary containing the extracted log record
            data with keys specified in self.keys plus the formatted message.
        """
        record = {key: getattr(data, key) for key in self.keys}
        if self.datefmt:
            created = record.get("created")
            record["created"] = datetime.fromtimestamp(created).strftime(
                self.datefmt,
            )
        record["message"] = data.getMessage()
        return record
