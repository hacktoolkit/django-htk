# Blob Storage App

Large binary data storage and retrieval (PDFs, images, archives, etc.).

## Quick Start

```python
from htk.apps.blob_storage.models import Blob

# Store binary data
blob = Blob.objects.create(
    name='document.pdf',
    data=pdf_bytes,
    content_type='application/pdf',
    user=request.user
)

# Retrieve data
blob = Blob.objects.get(id=blob_id)
binary_data = blob.data

# Delete blob
blob.delete()
```

## Storing Blobs

### Store File Content

```python
from htk.apps.blob_storage.models import Blob

# Store from file upload
uploaded_file = request.FILES['file']
blob = Blob.objects.create(
    name=uploaded_file.name,
    data=uploaded_file.read(),
    content_type=uploaded_file.content_type,
    user=request.user
)
```

### Store with Metadata

```python
from htk.apps.blob_storage.models import Blob

# Store with additional info
blob = Blob.objects.create(
    name='report.xlsx',
    data=excel_bytes,
    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    user=request.user,
    is_private=True,  # Access control
    metadata={
        'version': '1.0',
        'created_by': 'system',
        'source': 'export'
    }
)
```

### Store with Size Limit

```python
from htk.apps.blob_storage.models import Blob

MAX_BLOB_SIZE = 100 * 1024 * 1024  # 100MB

def store_blob_safe(file_obj, user, name):
    if file_obj.size > MAX_BLOB_SIZE:
        raise ValueError(f'File too large: {file_obj.size}')

    blob = Blob.objects.create(
        name=name,
        data=file_obj.read(),
        content_type=file_obj.content_type,
        user=user,
        size=file_obj.size
    )
    return blob
```

## Retrieving Blobs

### Get Blob by ID

```python
from htk.apps.blob_storage.models import Blob
from django.http import FileResponse

def download_blob(request, blob_id):
    blob = Blob.objects.get(id=blob_id)

    # Check access
    if blob.is_private and blob.user != request.user:
        raise PermissionDenied

    # Return file download
    response = FileResponse(blob.data)
    response['Content-Type'] = blob.content_type
    response['Content-Disposition'] = f'attachment; filename="{blob.name}"'
    return response
```

### List User's Blobs

```python
from htk.apps.blob_storage.models import Blob

# Get blobs for user
user_blobs = Blob.objects.filter(user=request.user)

# Filter by type
documents = user_blobs.filter(content_type='application/pdf')

# Get recent blobs
recent = user_blobs.order_by('-created')[:10]
```

## Common Patterns

### Virus Scanning

```python
from htk.apps.blob_storage.models import Blob
import subprocess

def scan_blob_for_virus(blob):
    """Scan uploaded file with ClamAV"""
    # Write to temp file
    import tempfile
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(blob.data)
        tmp.flush()

        # Run scan
        result = subprocess.run(
            ['clamscan', tmp.name],
            capture_output=True
        )

        return result.returncode == 0  # 0 = clean
```

### Compression

```python
import zlib
from htk.apps.blob_storage.models import Blob

def store_blob_compressed(data, name, user):
    """Store blob with compression"""
    compressed = zlib.compress(data)

    blob = Blob.objects.create(
        name=name,
        data=compressed,
        content_type='application/x-gzip',
        user=user,
        is_compressed=True,
        original_size=len(data),
        compressed_size=len(compressed)
    )
    return blob

def retrieve_blob_decompressed(blob):
    """Retrieve and decompress"""
    if blob.is_compressed:
        return zlib.decompress(blob.data)
    return blob.data
```

### S3 Storage Integration

```python
from htk.apps.blob_storage.models import Blob
from htk.lib.aws.s3.utils import S3Manager

def store_blob_to_s3(file_data, name, user):
    """Store blob to S3 instead of database"""
    s3 = S3Manager()

    # Upload to S3
    s3_path = f'blobs/{user.id}/{name}'
    s3.put_file('data-bucket', s3_path, file_data)

    # Create record pointing to S3
    blob = Blob.objects.create(
        name=name,
        s3_path=s3_path,  # Store reference instead of data
        content_type=content_type,
        user=user
    )
    return blob
```

### Expiring Blobs

```python
from django.utils import timezone
from datetime import timedelta
from htk.apps.blob_storage.models import Blob

def create_temporary_blob(data, name, user, ttl_hours=24):
    """Create blob that expires after TTL"""
    expiry = timezone.now() + timedelta(hours=ttl_hours)

    blob = Blob.objects.create(
        name=name,
        data=data,
        user=user,
        expires_at=expiry
    )
    return blob

def cleanup_expired_blobs():
    """Delete expired blobs"""
    Blob.objects.filter(
        expires_at__lt=timezone.now()
    ).delete()
```

### Access Control

```python
from htk.apps.blob_storage.models import Blob

def get_blob_safe(user, blob_id):
    """Get blob only if user has access"""
    blob = Blob.objects.get(id=blob_id)

    # Check ownership
    if blob.user != user:
        raise PermissionDenied('Cannot access this blob')

    # Check if private
    if blob.is_private and not blob.user.is_staff:
        raise PermissionDenied('Blob is private')

    return blob
```

## Models

### Blob

```python
class Blob(models.Model):
    user = ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = CharField(max_length=255)
    data = BinaryField()
    content_type = CharField(max_length=100)
    is_private = BooleanField(default=False)
    size = IntegerField()  # bytes
    expires_at = DateTimeField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
```

## Configuration

```python
# settings.py
BLOB_STORAGE_MAX_SIZE = 100 * 1024 * 1024  # 100MB
BLOB_STORAGE_ALLOWED_TYPES = [
    'application/pdf',
    'image/jpeg',
    'image/png',
    'application/zip',
]

BLOB_STORAGE_ENABLE_COMPRESSION = False
BLOB_STORAGE_ENABLE_S3 = False  # Use S3 instead of DB
BLOB_STORAGE_ENABLE_VIRUS_SCAN = False  # ClamAV scan
```

## Best Practices

1. **Validate file types** - Check MIME type and extension
2. **Scan for viruses** - Use ClamAV or similar
3. **Set size limits** - Prevent huge uploads
4. **Expire temporary files** - Clean up old blobs
5. **Use S3 for large files** - Database not ideal for large files
6. **Compress when appropriate** - Reduce storage
7. **Track access** - Log downloads

## Related Modules

- `htk.apps.file_storage` - File management
- `htk.lib.aws.s3` - S3 integration
- `htk.apps.accounts` - User management
