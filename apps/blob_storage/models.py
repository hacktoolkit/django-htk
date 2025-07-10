# Django Imports
from django.db import models
from django.http import (
    FileResponse,
    HttpResponse,
)

# HTK Imports
from htk.fields import CompressedBinaryField
from htk.utils import htk_setting


class AbstractBlobStorage(models.Model):
    content_type = models.CharField(max_length=64, blank=True)
    size_bytes = models.PositiveIntegerField(default=0)
    contents = CompressedBinaryField(
        max_length=htk_setting('HTK_BLOB_CONTENT_MAX_LENGTH'),
        editable=True,
    )

    class Meta:
        abstract = True

    @classmethod
    def create(cls, content_type='', contents=b''):
        size_bytes = len(contents)
        blob = cls.objects.create(
            content_type=content_type,
            size_bytes=size_bytes,
            contents=contents,
        )
        return blob

    def __str__(self):
        value = '{} - {}'.format(self.__class__.__name__, self.id)
        return value

    def update_contents(self, contents=b'', content_type=None):
        size_bytes = len(contents)
        self.size_bytes = size_bytes
        self.contents = contents
        if content_type is not None:
            self.content_type = content_type
        self.save()

    def as_response(self):
        response = HttpResponse(
            self.contents,
            content_type=self.content_type,
        )

        # Add CORS headers for images to allow social media platforms to access them
        if self.content_type.startswith('image/'):
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
            response['Access-Control-Allow-Headers'] = (
                'Accept, Accept-Language, Content-Language, Content-Type'
            )
            response['Access-Control-Max-Age'] = '86400'  # 24 hours
            # Add cache headers for better performance
            response['Cache-Control'] = (
                'public, max-age=86400, immutable'  # 24 hours
            )
            response['Vary'] = 'Accept-Encoding'

        # response = FileResponse(
        #     self.contents,
        #     as_attachment=True,
        #     filename='blob.jpeg'
        # )
        return response
