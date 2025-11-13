# AWS Integration

Amazon Web Services - S3, CloudFront, EC2, and more.

## S3 Storage

```python
from htk.lib.aws.s3.utils import S3Manager

s3 = S3Manager()

# Upload file
s3.put_file('my-bucket', 'path/file.jpg', file_obj)

# Get file URL
url = s3.get_url('my-bucket', 'path/file.jpg')

# Copy file
s3.copy_file('src-bucket', 'src-key', 'dest-bucket', 'dest-key')

# Delete file
s3.delete_file('my-bucket', 'path/file.jpg')
```

## S3 Media Assets

```python
from htk.lib.aws.s3.models import BaseS3MediaAsset

# Create media asset
asset = BaseS3MediaAsset.objects.create(
    s3_bucket='my-bucket',
    s3_key='images/photo.jpg'
)

# Store file
asset.store_file(file_obj)

# Get URL
url = asset.get_url()

# Clone asset
cloned = asset.clone()
```

## Configuration

```python
# settings.py
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = 'us-west-2'
AWS_S3_BUCKET_NAME = 'my-bucket'
```

## Caching

```python
from htk.lib.aws.s3.cachekeys import S3UrlCache

# URLs are cached for performance
cache = S3UrlCache('bucket', 'key')
url = cache.cache_get()
```

## Related Modules

- `htk.apps.file_storage` - File management
- `htk.apps.blob_storage` - Binary storage
