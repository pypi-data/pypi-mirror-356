# Azure Datalake Logging

**Log directly to Azure Storage services (Table, Blob, and Queue)**

Azure Datalake Logging provides Python logging handlers that integrate with Azure Storage services, allowing you to send log data directly to Azure without additional infrastructure.

## Features

- Direct logging to Azure Storage services
- Compatible with standard Python logging
- Support for structured data logging

## Supported Handlers

- [x] Table Storage
- [ ] Blob Storage *(coming soon)*
- [ ] Queue Storage *(coming soon)*


## Installation

```bash
pip install azure-datalake-logging
```

## Quick Start


### Table Storage Example

```py
from os import getenv

from azure.core.credentials import AzureNamedKeyCredential
import azure_datalake_logging as logging

name = __file__.removesuffix(".py")
logger = logging.getLogger(name)
logger.setLevel(logging.INFO)


account_name = getenv("STORAGE_ACCOUNT_NAME")
account_key = getenv("STORAGE_ACCOUNT_KEY")
credential = AzureNamedKeyCredential(account_name, account_key)

table_name = "DatalakeTableHandlerExample"

handler = logging.DatalakeTableHandler(account_name, table_name, credential)
handler.setLevel(logging.INFO)

formatter = logging.JsonFormatter()
handler.setFormatter(formatter)

logger.addHandler(handler)

# Log structured data
data = {"a": 1, "b": 2}
logger.info(data)

# Console output example (using JSONFormatter):
# {"created":"2023-06-15T10:23:45.123456","levelname":"INFO","lineno":29,"message":{"a":1,"b":2},"name":"example"}

# The following data structure is stored in Azure Table Storage.
# Each log entry contains these fields:
{
    "PartitionKey": "2023-06-15",   # Default: today's date
    "RowKey": "unique-id-12345",    # Auto-generated unique ID, UUID7 per default
    "level_number": 20,             # Numeric log level (20 for INFO)
    "level_name": "info",           # Text log level (lowercase)
    "module": "example_module",     # Source module name
    "line_number": 29,              # Source line number
    "function_name": "main",        # Source function name
    "message": "{\"a\":1,\"b\":2}"  # JSON-formatted message
}
```

## Standard Logging Compatibility

Azure Datalake Logging is fully compatible with the standard Python logging module:

```py
# Standard logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{name}.log"),
        logging.StreamHandler(),
    ],
)

logging.info("Test")
# 2025-04-06 09:39:56,644 - root - INFO - Test
```

## Configuration

Each handler requires Azure Storage credentials and specific configuration:

| Handler | Required Parameters |
|---------|-------------------|
| DatalakeTableHandler | `account_name`, `table_name` |


### DatalakeTableHandler Implementation Details

The `DatalakeTableHandler` provides flexible configuration options for logging to Azure Table Storage:

#### Constructor Parameters

```py
DatalakeTableHandler(
    account_name,             # Required: Azure Storage account name
    table_name,               # Required: Target table name
    credential=None,          # Optional: Azure credential object
    extra=None,               # Optional: `dict` Object with additional information to log
    part_key=None,            # Optional: Custom partition key (defaults to today's date)
    row_key_fn=None,          # Optional: Custom function for generating row keys
    to_stream=True,           # Optional: Whether to also log to console
)
```

#### Authentication Options

The handler supports multiple authentication methods:

- **Default Credentials**: If no credential is provided, DefaultAzureCredential is used
- **Named Key**: Use AzureNamedKeyCredential for account key authentication
- **SAS Token**: Use AzureSasCredential for SAS token authentication
- **Token Credential**: Use any Azure TokenCredential implementation

#### Advanced Configuration Examples

**Custom Partition and Row Keys:**

```py
import uuid
from datetime import datetime

# Use custom partition key (by month) and row key function
handler = logging.DatalakeTableHandler(
    account_name,
    table_name,
    credential=credential,
    part_key=datetime.now().strftime("%Y-%m"),
    row_key_fn=lambda: str(uuid.uuid4())
)
```

**Configure Additional Logging Options:**

```py
# Customize file and stream handlers
handler = logging.DatalakeTableHandler(
    account_name,
    table_name,
    credential=credential,
    to_stream=True,
)
```

**Azure Authentication with Named Key:**

```py
from azure.core.credentials import AzureNamedKeyCredential

# Using account name and key authentication
credential = AzureNamedKeyCredential(account_name, account_key)
handler = logging.DatalakeTableHandler(account_name, table_name, credential=credential)
```

#### Data Storage Format

Logs are stored in Azure Table Storage with the following structure:

- **PartitionKey**: Date by default (can be customized)
- **RowKey**: Auto-generated unique ID (can be customized)
- **Stored Fields**:
  - level_number: Numeric log level
  - level_name: Text log level (lowercase)
  - module: Source module name
  - line_number: Source line number
  - function_name: Source function name
  - message: Structured log message (JSON)

---

## Development Note

This package was developed with assistance from GitHub Copilot for:
- Generating docstrings
- Creating test cases

All AI-generated code has been thoroughly reviewed and validated for correctness, security, and performance.

---

## License

MIT License

Copyright (c) 2025 Markus Feiks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
