from abc import ABC, abstractmethod
from logging import NOTSET, Filter, Formatter, Handler, LogRecord


class BaseHandler(Handler, ABC):
    """
    Base handler class that implements the interface of logging.Handler
    and provides an abstract framework for Azure Data Lake logging handlers.
    """

    def __init__(self, level: int = NOTSET) -> None:
        """
        Initialize the handler with the specified logging level.

        Args:
            level: The logging level threshold
        """
        super().__init__(level)

    @abstractmethod
    def emit(self, record: LogRecord) -> None:
        """
        Abstract method that handles the actual logging of a LogRecord.

        Args:
            record: The log record to be processed

        Raises:
            NotImplementedError: If not implemented by subclasses
        """
        raise NotImplementedError

    def handle(self, record: LogRecord) -> bool:
        """
        Conditionally emit the specified logging record.

        Args:
            record: The log record to be processed

        Returns:
            True if the record was handled successfully
        """
        return super().handle(record)

    def createLock(self) -> None:
        """Create a thread lock for serializing access to the handler."""
        super().createLock()

    def acquire(self) -> None:
        """Acquire the handler's lock."""
        super().acquire()

    def release(self) -> None:
        """Release the handler's lock."""
        super().release()

    def setLevel(self, level: int) -> None:
        """
        Set the logging level of this handler.

        Args:
            level: The logging level to set
        """
        super().setLevel(level)

    def setFormatter(self, formatter: Formatter) -> None:
        """
        Set the formatter for this handler.

        Args:
            formatter: The formatter to use
        """
        super().setFormatter(formatter)

    def addFilter(self, filter_obj: Filter) -> None:
        """
        Add the specified filter to this handler.

        Args:
            filter_obj: The filter to add
        """
        super().addFilter(filter_obj)

    def removeFilter(self, filter_obj: Filter) -> None:
        """
        Remove the specified filter from this handler.

        Args:
            filter_obj: The filter to remove
        """
        super().removeFilter(filter_obj)

    def filter(self, record: LogRecord) -> bool:
        """
        Apply filters to the record and return True
        if the record should be processed.

        Args:
            record: The log record to filter

        Returns:
            True if the record should be processed
        """
        return super().filter(record)

    def flush(self) -> None:
        """
        Ensure all logging output has been flushed.
        This is a no-op by default and should be
        implemented by subclasses if needed.
        """
        pass

    def close(self) -> None:
        """
        Clean up any resources used by the handler.
        This is a no-op by default and should be
        implemented by subclasses if needed.
        """
        super().close()

    def handleError(self, record: LogRecord) -> None:
        """
        Handle errors which occur during emit() calls.

        Args:
            record: The log record that triggered the error
        """
        super().handleError(record)

    def format(self, record: LogRecord) -> str:
        """
        Format the specified record.

        Args:
            record: The log record to format

        Returns:
            A formatted string
        """
        if self.formatter:
            return self.formatter.format(record)
        return record.getMessage()
