# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.db import models

# HTK Imports
from htk.constants import *
from htk.lib.aws.s3 import S3Manager
from htk.utils import htk_setting
from htk.utils.request import get_current_request
from htk.utils.s3 import get_env_s3_key_prefix


THUMBNAIL_KEY_SUFFIX = '_thumbnail'


class S3MediaAsset(models.Model):
    class Meta:
        abstract = True

    def get_media_type(self):
        media_type  = self.__class__.__name__
        return media_type

    def get_s3_key(self, suffix=None):
        """Computes the S3 Key for this object

        Must be saved in database already, because the S3 Key depends on the object id
        """
        if suffix is None:
            suffix = ''

        s3_key_config = {
            'env': get_env_s3_key_prefix(),
            'type': self.get_media_type(),
            'id': self.id,
            'suffix': suffix,
        }
        s3_key = '%(env)s/%(type)s/%(id)d%(suffix)s' % s3_key_config
        return s3_key

    def get_s3_bucket(self):
        s3_bucket = htk_setting('HTK_S3_BUCKET', None)
        if not s3_bucket:
            raise Exception('Missing S3 Bucket')
        return s3_bucket

    def get_s3_url(self, key_suffix=None):
        try:
            s3 = S3Manager()

            s3_bucket = self.get_s3_bucket()
            s3_key = self.get_s3_key(suffix=key_suffix)

            if s3.key_exists(s3_bucket, s3_key):
                s3_url = s3.get_url(s3_bucket, s3_key, cache=True)
            else:
                s3_url = None
        except Exception:
            request = get_current_request()
            rollbar.report_exc_info(request=request)
            s3_url = None
        return s3_url

    def get_thumbnail_url(self, key_suffix=THUMBNAIL_KEY_SUFFIX):
        s3_url = self.get_s3_url(key_suffix=key_suffix)
        return s3_url

    def has_thumbnail(self, key_suffix=THUMBNAIL_KEY_SUFFIX):
        s3 = S3Manager()

        s3_bucket = self.get_s3_bucket()
        s3_key = self.get_s3_key(suffix=key_suffix)

        return s3.key_exists(s3_bucket, s3_key)

    def store_file(self, f, key_suffix=None):
        """Stores file `f`
        """
        s3 = S3Manager()

        s3_bucket = self.get_s3_bucket()
        s3_key = self.get_s3_key(suffix=key_suffix)

        bytes_written = s3.put_file(s3_bucket, s3_key, f)
        # self.is_s3 = True
        # self.orig_filename = f.name
        # self.file_mime_type = f.content_type
        # self.file_charset = f.charset if f.charset else ''
        # self.file_size_bytes = f.size
        # self.s3_bytes = bytes_written
        self.save()

    def store_uploaded_file(self, f):
        """Store the uploaded file
        """
        self.store_file(f)

    def store_thumbnail(self, f, key_suffix=THUMBNAIL_KEY_SUFFIX):
        self.store_file(f, key_suffix=key_suffix)

    def copy_stored_file_to(self, dest_obj, key_suffix=None):
        """Copies the stored file on S3 into the `dest_obj`'s bucket/key
        """
        s3 = S3Manager()

        src_bucket_id = self.get_s3_bucket()
        src_key_id = self.get_s3_key(suffix=key_suffix)

        dest_bucket_id = dest_obj.get_s3_bucket()
        dest_key_id = dest_obj.get_s3_key(suffix=key_suffix)

        was_copied = s3.copy_file(src_bucket_id, src_key_id, dest_bucket_id, dest_key_id)
        return was_copied

    def delete_asset(self, thumbnail_key_suffix=THUMBNAIL_KEY_SUFFIX, force=False):
        was_deleted = self.delete_stored_file()

        if was_deleted and self.has_thumbnail(key_suffix=THUMBNAIL_KEY_SUFFIX):
            was_deleted = self.delete_thumbnail(key_suffix=thumbnail_key_suffix)

        if was_deleted or force:
            self.delete()

    def delete_stored_file(self, key_suffix=None):
        was_deleted = False
        try:
            s3 = S3Manager()

            s3_bucket = self.get_s3_bucket()
            s3_key = self.get_s3_key(suffix=key_suffix)

            was_deleted = s3.delete_file(s3_bucket, s3_key)
        except Exception:
            request = get_current_request()
            rollbar.report_exc_info(request=request)
            was_deleted = False
        return was_deleted

    def delete_thumbnail(self, key_suffix=THUMBNAIL_KEY_SUFFIX):
        """Convenience wrapper around `self.delete_stored_file()` to delete a thumbnail, if one exists
        """
        self.delete_stored_file(key_suffix=key_suffix)

    def clone(self, thumbnail_key_suffix=THUMBNAIL_KEY_SUFFIX, delete_on_failure=False):
        """Makes a clone of this S3MediaAsset with a copied file on S3
        """
        cloned_obj = self.__class__.objects.create()
        was_copied = self.copy_stored_file_to(cloned_obj)

        if was_copied and self.has_thumbnail(key_suffix=thumbnail_key_suffix):
            was_copied = self.copy_stored_file_to(cloned_obj, key_suffix=thumbnail_key_suffix)

        if not was_copied:
            cloned_obj.delete_asset(force=True)
            cloned_obj = None

            if delete_on_failure:
                self.delete_asset(force=True)
        else:
            pass

        return cloned_obj
