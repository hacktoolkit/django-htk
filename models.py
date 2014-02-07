from django.db import models

"""
While we *could* import models here for convenience,
we must also remember to be careful to not assume that the external dependencies will be met for every platform, so it's better to import only what's needed explicitly

For example, the following module requires AWS Credentials.
  from htk.lib.aws.s3.models import S3MediaAsset

Others, like imaging libraries, require PIL, etc
"""
