# File Storage App

File upload and storage management.

## Quick Start

```python
from htk.apps.file_storage.utils import store_uploaded_file

# Store uploaded file
file_obj = request.FILES['file']
stored_file = store_uploaded_file(file_obj, folder='uploads')

path = stored_file.path
url = stored_file.url
```

## Common Patterns

```python
# Store with custom path
from htk.apps.file_storage.models import StoredFile

file = StoredFile.objects.create(
    file=uploaded_file,
    user=request.user,
    folder='documents'
)

# Delete file
file.delete()  # Removes from disk and DB
```

## Configuration

```python
# settings.py
FILE_STORAGE_PATH = 'uploads/'
FILE_STORAGE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx']
```

## Related Modules

- `htk.apps.blob_storage` - Binary storage
- `htk.lib.aws.s3` - Cloud storage
