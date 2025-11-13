# Blob Storage Constants

## Overview

This module defines configuration for the blob storage system, which handles large binary data objects.

## Constants

### Storage Configuration

- **`HTK_BLOB_CONTENT_MAX_LENGTH`** - Maximum size of blob content in bytes. Default: `10485760` (10 MB)

## Usage Examples

### Validate Blob Size

```python
from htk.apps.blob_storage.constants import HTK_BLOB_CONTENT_MAX_LENGTH

file_size = os.path.getsize('large_file.bin')
if file_size > HTK_BLOB_CONTENT_MAX_LENGTH:
    raise ValueError(f'File exceeds {HTK_BLOB_CONTENT_MAX_LENGTH} bytes')
```

### Configure Max Size

```python
# In Django settings.py
HTK_BLOB_CONTENT_MAX_LENGTH = 50 * 1000 * 1000  # 50 MB
```
