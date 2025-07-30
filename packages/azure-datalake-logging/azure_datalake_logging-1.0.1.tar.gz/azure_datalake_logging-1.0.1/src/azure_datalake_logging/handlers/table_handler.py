import json
from ast import literal_eval
from collections.abc import Callable
from datetime import date
from logging import FileHandler, LogRecord, StreamHandler
from typing import TypeAlias

from azure.core.credentials import (
    AzureNamedKeyCredential,
    AzureSasCredential,
    TokenCredential,
)
from azure.core.exceptions import ResourceExistsError
from azure.data.tables import TableClient
from azure.identity import DefaultAzureCredential

from ..utils import create_id

TableCredential: TypeAlias = (
    AzureSasCredential
    | AzureNamedKeyCredential
    | TokenCredential
    | DefaultAzureCredential
)


class TableClientMock:
    def __init__(
        self,
        endpoint: str,
        table_name: str,
        *,
        credential=None,
        api_version=None,
        **kwargs,
    ):
        self.endpoint = endpoint
        self.table_name = table_name
        self.credential = credential
        self.api_version = api_version

    def create_table(self):
        return self

    def create_entity(self, data: dict):
        print(f"{data}")


class DatalakeTableHandler(StreamHandler):
    def __init__(
        self,
        account_name: str,
        table_name: str,
        credential: TableCredential | None = None,
        *,
        extra: dict = None,
        part_key: str = None,
        row_key_fn: Callable = None,
        to_stream: bool = True,
    ):
        super().__init__()
        self.account_name = account_name
        self.endpoint = f"https://{self.account_name}.table.core.windows.net"
        self.table_name = table_name
        self.credential = credential or DefaultAzureCredential()
        self.part_key = part_key or str(date.today())
        self.extra = extra if isinstance(extra, dict) else {}
        self.row_key_fn = self._set_row_key_fn(row_key_fn)
        self.table = self._setup_table()
        self.to_stream = to_stream

    def emit(self, record: LogRecord) -> str:
        """
        Emit a log record.

        This method formats the log record, sends it to the configured stream
        and file handlers, and creates an entity in the Azure Table Storage.

        Args:
            record: LogRecord object containing the log information

        Returns:
            str: The formatted log message
        """
        record_dict = {
            "level_number": record.levelno,
            "level_name": record.levelname.lower(),
            "module": record.module,
            "line_number": record.lineno,
            "function_name": record.funcName,
            "message": record.getMessage(),
            **self.extra,
            # "created": record.created,
            # "asctime": self.formatter.formatTime(record,
            # "msecs": record.msecs,
            # "name": record.name,
            # "pathname": record.pathname,
            # "filename": record.filename,
            # "relativeCreated": record.relativeCreated,
            # "thread": record.thread,
            # "threadName": record.threadName,
            # "process": record.process,
        }
        if self.to_stream:
            super().emit(record)
        entity = self._create_table_entity(record_dict)
        self.table.create_entity(entity)

    def _setup_table(self) -> TableClient:
        """
        Initialize and create an Azure Table Storage table if it doesn't exist.

        Creates a connection to the table specified in the handler configuration.
        If the table doesn't exist, it will be created. If it already exists,
        the function will silently continue using the existing table.

        Returns:
            TableClient: Initialized Azure Table Storage client
        """
        table = TableClient(
            self.endpoint,
            self.table_name,
            credential=self.credential,
        )
        try:
            table.create_table()
        except ResourceExistsError:
            pass
        return table

    def _set_row_key_fn(self, fn: Callable = None) -> Callable:
        """
        Set the function used to generate row keys for table entities.

        Args:
            fn: Custom function to generate row keys. If None or not callable,
                defaults to the create_id function.

        Returns:
            Callable: The function that will be used to generate row keys
        """
        return fn if isinstance(fn, Callable) else create_id

    def _setup_stream_handler(self, config: dict = None) -> StreamHandler:
        """
        Initialize a StreamHandler for console logging.

        Args:
            config: Dictionary containing configuration options for the
                   StreamHandler. If None, default configuration is used.

        Returns:
            StreamHandler: Configured handler for console output
        """
        return StreamHandler(**(config or {}))

    def _setup_file_handler(self, config: dict = None) -> FileHandler:
        """
        Initialize a FileHandler for file-based logging.

        Args:
            config: Dictionary containing configuration options for the
                   FileHandler. If None, defaults to using 'app.log' as filename.

        Returns:
            FileHandler: Configured handler for file output
        """
        config = {"filename": "app.log", **(config or {})}
        return FileHandler(**config)

    def _create_table_entity(self, data: dict) -> dict:
        """
        Create an entity for Azure Table Storage from log record data.

        This method transforms log data into the format required for Azure Table
        Storage, extracting the message field for special processing and adding
        required partition and row keys.

        Args:
            data: Dictionary containing log record data

        Returns:
            Dictionary formatted as an Azure Table Storage entity
        """
        message = data.pop("message")

        # Handle both string messages and stringified Python dictionaries
        try:
            # Try to evaluate as a Python literal (dict, list, etc.)
            parsed_message = literal_eval(message)
            message = json.dumps(parsed_message)
        except (ValueError, SyntaxError):
            # If it's not a valid Python literal, treat as plain string
            message = json.dumps(message)

        return {
            "PartitionKey": self.part_key,
            "RowKey": create_id(),
            **data,
            "message": message,
        }
