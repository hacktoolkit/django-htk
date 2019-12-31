import re
import time

from boto.exception import S3ResponseError
from boto.s3.connection import S3Connection
from boto.s3.bucket import Bucket
from boto.s3.key import Key

from htk.lib.aws.s3.cachekeys import S3UrlCache
from htk.constants.time import *

class S3Manager(object):
    """S3Manager is an interface/wrapper for boto to Amazon S3
    """
    def __init__(self):
        try:
            # AWSCredentials should be available in settings.CREDENTIALS_DIR
            import AWSCredentials
            self.access_key = AWSCredentials.HEADLESS_S3_ACCESS_KEY
            self.secret_key = AWSCredentials.HEADLESS_S3_SECRET_KEY
            self._connect()
        except:
            print('Unable to connect to AWS or missing AWSCredentials')

    def _connect(self):
        self.conn = S3Connection(self.access_key, self.secret_key)

    def _get_bucket(self, bucket_id, validate=True):
        """Returns a boto.s3.bucket.Bucket object pointing at S3:bucket-id
        """
        try:
            bucket = self.conn.get_bucket(bucket_id, validate=validate)
        except S3ResponseError:
            bucket = None
        return bucket

    def _get_key(self, bucket_id, key_id, validate_bucket=True, validate_key=False):
        """Returns a boto.s3.key.Key object pointing at S3:bucket-id/key-id
        """
        bucket = self._get_bucket(bucket_id, validate=validate_bucket)
        if bucket:
            key = bucket.get_key(key_id, validate=validate_key)
        else:
            key = None
        return key

    def put_file(self, bucket_id, key_id, f):
        """Stores a file
        """
        prekey = [bucket_id, key_id,]
        c = S3UrlCache(prekey)
        c.invalidate_cache()
        key = self._get_key(bucket_id, key_id)
        if key:
            bytes_written = key.set_contents_from_file(f)
        else:
            bytes_written = 0
        return bytes_written

    def key_exists(self, bucket_id, key_id):
        key = self._get_key(bucket_id, key_id, validate_key=True)
        result = key is not None
        return result

    def copy_file(self, src_bucket_id, src_key_id, dest_bucket_id, dest_key_id):
        """Copies a file
        """
        src_key = self._get_key(src_bucket_id, src_key_id)
        new_key = src_key.copy(dest_bucket_id, dest_key_id)

    def delete_file(self, bucket_id, key_id):
        """Deletes a file
        """
        key = self._get_key(bucket_id, key_id)
        was_deleted = False
        if key:
            key.delete()
            was_deleted = True
        return was_deleted

    def get_url(self, bucket_id, key_id, expiration=3600, cache=False):
        """Generates the URL for a file

        `expiration` how long we should request for
        `cache` if we should read/write the value from/to cache
        """
        if cache:
            prekey = [bucket_id, key_id,]
            c = S3UrlCache(prekey)
            url = c.get()
        else:
            url = None

        if url is None:
            key = self._get_key(bucket_id, key_id)
            if key:
                url = key.generate_url(expiration)
                if cache:
                    # need to check the actual URL expiration
                    expiration_match = re.match(r'.*&Expires=(\d)+&.*', url)
                    if expiration_match:
                        expires_at = expiration_match.group(1)
                        # request slightly shorter cache duration to have a buffer; at least 1 minute
                        duration = max(int(expires_at) - int(time.time()) - TIMEOUT_5_MINUTES, TIMEOUT_1_MINUTE)
                    else:
                        duration = None
                    c.cache_store(url, duration)
            else:
                url = None
        return url
