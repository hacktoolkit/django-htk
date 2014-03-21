import rollbar

from django.db import models

from htk.constants import *
from htk.lib.aws.s3 import S3Manager
from htk.middleware import GlobalRequestMiddleware
from htk.utils import htk_setting
from htk.utils.s3 import get_env_s3_key_prefix

class S3MediaAsset(models.Model):
    class Meta:
        abstract = True

    def get_media_type(self):
        media_type  = self.__class__.__name__
        return media_type

    def get_s3_key(self):
        """Computes the S3 Key for this object

        Must be saved in database already, because the S3 Key depends on the object id
        """
        s3_key_config = {
            'env' : get_env_s3_key_prefix(),
            'type' : self.get_media_type(),
            'id' : self.id,
        }
        s3_key = '%(env)s/%(type)s/%(id)d' % s3_key_config
        return s3_key

    def get_s3_bucket(self):
        s3_bucket = htk_setting('HTK_S3_BUCKET', None)
        if not s3_bucket:
            raise Exception('Missing S3 Bucket')
        return s3_bucket

    def get_s3_url(self):
        try:
            s3 = S3Manager()
            s3_bucket = self.get_s3_bucket()
            s3_key = self.get_s3_key()
            s3_url = s3.get_url(s3_bucket, s3_key, cache=True)
        except:
            request = GlobalRequestMiddleware.get_current_request()
            rollbar.report_exc_info(request=request)
            s3_url = ''
        return s3_url

    def store_uploaded_file(self, f):
        """Store the uploaded file
        """
        s3_bucket = self.get_s3_bucket()
        s3_key = self.get_s3_key()
        s3 = S3Manager()
        bytes_written = s3.put_file(s3_bucket, s3_key, f)
#        self.is_s3 = True
#        self.orig_filename = f.name
#        self.file_mime_type = f.content_type
#        self.file_charset = f.charset if f.charset else ''
#        self.file_size_bytes = f.size
#        self.s3_bytes = bytes_written
        self.save()

    def copy_stored_file_to(self, dest_obj):
        """Copies the stored file on S3 into the `dest_obj`'s bucket/key
        """
        src_bucket_id = self.get_s3_bucket()
        src_key_id = self.get_s3_key()
        dest_bucket_id = dest_obj.get_s3_bucket()
        dest_key_id = dest_obj.get_s3_key()
        s3 = S3Manager()
        s3.copy_file(src_bucket_id, src_key_id, dest_bucket_id, dest_key_id)

    def delete_stored_file(self):
        # TODO: not implemented yet
        s3 = S3Manager()
        pass

    def clone(self):
        """Makes a clone of this S3MediaAsset with a copied file on S3
        """
        cloned_obj = self.__class__.objects.create()
        self.copy_stored_file_to(cloned_obj)
        return cloned_obj
