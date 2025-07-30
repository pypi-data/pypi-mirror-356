import json
from collections.abc import Callable
from logging import LogRecord

from .struct_formatter import StructFormatter


class JsonFormatter(StructFormatter):
    """
    Formats input data as a JSON string.

    This formatter converts Python dictionaries or other serializable
    objects into valid JSON strings.
    """

    def __init__(
        self,
        keys: str | list[str] | set[str] = None,
        *,
        sort_keys: bool = True,
        fmt: str = None,
        datefmt: str = None,
        ensure_ascii: bool = False,
        indent: int = None,
        default: Callable = str,
        separators: tuple[str, str] = (",", ":"),
    ) -> None:
        """
        Initialize the JSON formatter with configuration options.

        Args:
            keys: Keys to include in the output.
                Can be a single string, comma-separated string,
                a list of strings, or a set of strings.
                If None, all keys will be included.
            datefmt: Format string for datetime objects.
                If None, a Timestamp will be returned.
            sort_keys: Whether to sort the JSON keys alphabetically.
            ensure_ascii:
                If True, non-ASCII characters in the output are escaped.
                If False, UTF-8 characters pass through unchanged.
            indent: Number of spaces for indentation in the output JSON.
                If None, the output will be compact without extra whitespace.
            default: Function to convert non-serializable objects to strings.
                Defaults to the str() function.
            separators: Tuple of strings.
                Defaults to (',', ':') to eliminate whitespace.

        """

        super().__init__(keys=keys, datefmt=datefmt, fmt=fmt)

        # json.dumps options
        self.ensure_ascii = ensure_ascii
        self.indent = indent
        self.default = default
        self.sort_keys = sort_keys
        self.separators = separators

    def format(self, data: LogRecord) -> str:
        """
        Convert input data to a JSON string.

        Args:
            data: Dictionary containing data to be formatted as JSON

        Returns:
            A valid JSON string representation of the input data

        Raises:
            TypeError: If the data cannot be serialized to JSON
        """

        try:
            record = self._create_record(data)
            record = self._validate(record)

            return json.dumps(
                record,
                indent=self.indent,
                ensure_ascii=self.ensure_ascii,
                default=self.default,
                sort_keys=self.sort_keys,
                separators=self.separators,
            )

        except TypeError as e:
            msg = "Unable to serialize data to JSON format"
            raise TypeError(msg) from e

    def _validate(self, record: dict) -> dict:
        for key, value in record.items():
            try:
                json.dumps(value)
            except TypeError as e:
                msg = f"Unable to serialize data to JSON format: {key}"
                raise TypeError(msg) from e
        return record
