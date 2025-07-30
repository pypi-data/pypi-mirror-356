# azure-datalake-logging

## Features
Azure Datalake Gen2 hat bietet unterschiedliche Speicheroptionen:
- Blob
- Queue
- Table
- File

Dieses Python Package soll für `Blob`, `Queue` und `Table` Speicher jeweils einen `logging.Handler` bereitstellen, der mit dem Standard `logging` module kompatibel ist.

```py

import azure_datalake_logging as logging

logger = logging.getLogger(__name__)
table_handler = logging.TableHandler()
logger.addHandler(TableHandler)
```