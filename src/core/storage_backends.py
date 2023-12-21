from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class S3StaticStorage(S3Boto3Storage):
    # location = "static"
    default_acl = "public-read"
    bucket_name = settings.S3_STATIC_BUCKET_NAME


class S3MediaStorage(S3Boto3Storage):
    # location = "media"
    default_acl = "private"
    bucket_name = settings.S3_MEDIA_BUCKET_NAME
