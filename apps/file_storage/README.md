File Storage
============

App for managing local file-system storage.

This kinda works for small amounts of file storage, but is not really scalable unless we have a comprehensive strategy for disk space allocation and backups.

It's better to just use something like htk.lib.aws.s3.models.S3MediaAsset for cloud-based storage
