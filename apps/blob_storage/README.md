# Blob Storage App

Large binary data storage and retrieval.

## Quick Start

```python
from htk.apps.blob_storage.models import Blob

# Store binary data
blob = Blob.objects.create(
    name='document.pdf',
    data=pdf_bytes,
    content_type='application/pdf'
)

# Retrieve
blob = Blob.objects.get(name='document.pdf')
binary_data = blob.data
```

## Models

- **`Blob`** - Binary large object storage

## Common Patterns

```python
# Store with access control
blob = Blob.objects.create(
    name='private.zip',
    data=file_bytes,
    user=request.user,
    is_private=True
)

# Get blob by ID
blob = Blob.objects.get(id=blob_id)
```

## Related Modules

- `htk.apps.file_storage` - File management
- `htk.lib.aws.s3` - S3 integration
