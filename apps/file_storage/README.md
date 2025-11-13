# File Storage App

File upload, storage, and management with Django file fields.

## Quick Start

```python
from htk.apps.file_storage.models import StoredFile
from htk.apps.file_storage.utils import store_uploaded_file

# Store uploaded file
file_obj = request.FILES['file']
stored_file = store_uploaded_file(file_obj, folder='uploads', user=request.user)

# Access file
print(stored_file.file.path)  # Disk path
print(stored_file.file.url)   # Web URL

# Delete file
stored_file.delete()  # Removes from disk and DB
```

## File Upload

### Basic File Storage

```python
from htk.apps.file_storage.models import StoredFile

# Store uploaded file
uploaded_file = request.FILES['document']
stored = StoredFile.objects.create(
    file=uploaded_file,
    user=request.user,
    folder='documents'
)

# Access URL for display
url = stored.file.url
```

### With Validation

```python
from django.core.exceptions import ValidationError
from htk.apps.file_storage.utils import store_uploaded_file

ALLOWED_TYPES = ['pdf', 'doc', 'docx', 'txt']
MAX_SIZE = 10 * 1024 * 1024  # 10MB

def upload_document(file_obj, user):
    # Check size
    if file_obj.size > MAX_SIZE:
        raise ValidationError(f'File too large: {file_obj.size}')

    # Check type
    ext = file_obj.name.split('.')[-1].lower()
    if ext not in ALLOWED_TYPES:
        raise ValidationError(f'File type not allowed: {ext}')

    # Store file
    stored = store_uploaded_file(file_obj, folder='documents', user=user)
    return stored
```

### Organize by Folder

```python
from htk.apps.file_storage.models import StoredFile

# Store in organized structure
uploaded = request.FILES['file']

# Store with folder
stored = StoredFile.objects.create(
    file=uploaded,
    user=request.user,
    folder=f'{request.user.id}/documents/{timezone.now().year}'
)
```

## File Management

### List Files

```python
from htk.apps.file_storage.models import StoredFile

# Get user's files
user_files = StoredFile.objects.filter(user=request.user)

# Filter by folder
documents = StoredFile.objects.filter(
    user=request.user,
    folder__startswith='documents'
)

# Get recent files
recent = user_files.order_by('-created')[:20]
```

### Download Files

```python
from django.http import FileResponse
from htk.apps.file_storage.models import StoredFile

def download_file(request, file_id):
    stored_file = StoredFile.objects.get(id=file_id)

    # Check access
    if stored_file.user != request.user:
        raise PermissionDenied

    # Return file
    response = FileResponse(stored_file.file.open('rb'))
    response['Content-Type'] = stored_file.get_mime_type()
    response['Content-Disposition'] = f'attachment; filename="{stored_file.file.name}"'
    return response
```

### Delete Files

```python
from htk.apps.file_storage.models import StoredFile

# Delete single file
stored_file = StoredFile.objects.get(id=file_id)
stored_file.delete()  # Removes from disk and DB

# Delete multiple files
StoredFile.objects.filter(
    user=request.user,
    created__lt=timezone.now() - timedelta(days=30)
).delete()
```

## Common Patterns

### File Validation

```python
import os
from django.core.exceptions import ValidationError
from htk.apps.file_storage.models import StoredFile

ALLOWED_EXTENSIONS = ['pdf', 'txt', 'doc', 'docx', 'xls', 'xlsx']
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def validate_file(file_obj):
    # Check size
    if file_obj.size > MAX_FILE_SIZE:
        raise ValidationError('File is too large')

    # Check extension
    ext = os.path.splitext(file_obj.name)[1].lower().lstrip('.')
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'File type {ext} not allowed')

    return True
```

### Image Thumbnail Generation

```python
from PIL import Image
from io import BytesIO
from htk.apps.file_storage.models import StoredFile

def generate_thumbnail(stored_file, size=(200, 200)):
    """Generate thumbnail for image file"""
    if not stored_file.is_image():
        return None

    img = Image.open(stored_file.file)
    img.thumbnail(size)

    thumb_io = BytesIO()
    img.save(thumb_io, format='JPEG')
    thumb_io.seek(0)

    # Store thumbnail
    thumb = StoredFile.objects.create(
        file=thumb_io,
        user=stored_file.user,
        folder=f'{stored_file.folder}/thumbnails',
        parent=stored_file
    )
    return thumb
```

### File Versioning

```python
from htk.apps.file_storage.models import StoredFile

def store_file_with_version(file_obj, name, user, folder):
    """Store file with automatic versioning"""
    existing = StoredFile.objects.filter(
        name=name,
        folder=folder,
        user=user
    ).order_by('-version').first()

    version = (existing.version if existing else 0) + 1

    stored = StoredFile.objects.create(
        file=file_obj,
        name=f'{name}.v{version}',
        user=user,
        folder=folder,
        version=version,
        parent=existing
    )
    return stored
```

### Storage Quota

```python
from django.db.models import Sum
from htk.apps.file_storage.models import StoredFile

USER_STORAGE_QUOTA = 1024 * 1024 * 1024  # 1GB

def check_storage_quota(user):
    """Check if user exceeds storage quota"""
    total_size = StoredFile.objects.filter(
        user=user
    ).aggregate(total=Sum('file__size'))['total'] or 0

    return total_size < USER_STORAGE_QUOTA

def get_user_storage_usage(user):
    """Get formatted storage usage"""
    total_bytes = StoredFile.objects.filter(
        user=user
    ).aggregate(total=Sum('file__size'))['total'] or 0

    return {
        'used_bytes': total_bytes,
        'quota_bytes': USER_STORAGE_QUOTA,
        'used_percent': (total_bytes / USER_STORAGE_QUOTA) * 100,
        'used_gb': total_bytes / (1024**3),
        'quota_gb': USER_STORAGE_QUOTA / (1024**3)
    }
```

### Bulk Operations

```python
from htk.apps.file_storage.models import StoredFile

def export_user_files(user):
    """Create ZIP of all user files"""
    import zipfile
    from io import BytesIO

    files = StoredFile.objects.filter(user=user)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for stored_file in files:
            zip_file.writestr(
                stored_file.file.name,
                stored_file.file.read()
            )

    zip_buffer.seek(0)
    return zip_buffer
```

## Models

### StoredFile

```python
class StoredFile(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    file = FileField(upload_to='files/%Y/%m/%d/')
    name = CharField(max_length=255)
    folder = CharField(max_length=255, default='')
    size = IntegerField()  # bytes
    mime_type = CharField(max_length=100)
    version = IntegerField(default=1)
    parent = ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
```

## Configuration

```python
# settings.py
FILE_STORAGE_PATH = 'files/'
FILE_STORAGE_MAX_SIZE = 50 * 1024 * 1024  # 50MB per file

ALLOWED_FILE_TYPES = [
    'application/pdf',
    'text/plain',
    'application/msword',
    'image/jpeg',
    'image/png',
]

# Storage backend
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'LOCATION': os.path.join(BASE_DIR, 'media')
    }
}
```

## Best Practices

1. **Validate files** - Check type and size before storing
2. **Organize by user** - Separate storage by user for security
3. **Set size limits** - Prevent excessive storage usage
4. **Use relative URLs** - Reference by URL, not path
5. **Cleanup old files** - Delete expired/unused files
6. **Version files** - Track changes with versions
7. **Test with S3** - Use cloud storage in production
