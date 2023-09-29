import json
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from minio import Minio

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Will be executed with:
    ~~~
    python manage.py createbuckets
    ~~~
    """

    help = "Create static and media minio buckets"

    public_read_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                "Resource": "arn:aws:s3:::{}".format(
                    settings.S3_STATIC_BUCKET_NAME
                ),
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::{}/*".format(
                    settings.S3_STATIC_BUCKET_NAME
                ),
            },
        ],
    }

    def handle(self, *args, **options):
        minio_client = Minio(
            endpoint=settings.S3_STORAGE_ENDPOINT,
            access_key=settings.S3_STORAGE_ACCESS_KEY,
            secret_key=settings.S3_STORAGE_SECRET_KEY,
            secure="https" in settings.S3_URL,
        )
        minio_client.make_bucket(settings.S3_STATIC_BUCKET_NAME)
        minio_client.set_bucket_policy(
            settings.S3_STATIC_BUCKET_NAME, json.dumps(
                self.public_read_policy)
        )
        minio_client.make_bucket(settings.S3_MEDIA_BUCKET_NAME)
        print("Buckets succesfully created")
