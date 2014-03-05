import hashlib
import os

from django.conf import settings

from htk.apps.file_storage.constants import *

def get_filesystem_path(file_name, file_type, file_id):
    # MEDIA_ROOT = os.path.join(BASEDIR, 'uploads')
    base_dir = settings.MEDIA_ROOT
    relative_path = _get_file_path_relative(file_name, file_type, file_id)
    filesystem_path = '%s/%s' % (
        base_dir,
        relative_path,
    )
    return filesystem_path

def get_web_path(file_name, file_type, file_id):
    web_root = settings.MEDIA_URL
    relative_path = _get_file_path_relative(file_name, file_type, file_id)
    web_path = os.path.join(web_root, relative_path)
    return web_path

def _get_file_extension(file_name):
    file_extension = os.path.splitext(file_name)[1]
    return file_extension

def _get_file_path_relative(file_name, file_type, file_id):
    """
    file_type is a string identifier for a type of file in our application, for example, 'logo' or 'repository'
    file_id is a unique id for this `file_type`
    file_extension is the file extension of the file
    """
    # store it in one of 256 buckets, 00-ff
    file_extension = _get_file_extension(file_name)
    filename = '%s_%s%s' % (file_type, file_id, file_extension)
    file_storage_secret = htk_setting('HTK_FILE_STORAGE_SECRET')
    prehash = '%s_%s' % (FILE_STORAGE_SECRET, filename,)
    #path = '%02x' % (file_id % 255)
    path = hashlib.md5(prehash).hexdigest()[:2]
    file_path = '%s/%s' % (
        path,
        filename,
    )
    return file_path

def store_uploaded_file(f, file_type, file_id):
    """Store the uploaded file

    https://docs.djangoproject.com/en/dev/topics/http/file-uploads/
    """
    file_path = get_filesystem_path(f.name, file_type, file_id)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True

def create_directories():
    for x in xrange(256):
        dirname = '%s/%02x' % (settings.MEDIA_ROOT, x)
        os.mkdir(dirname)
