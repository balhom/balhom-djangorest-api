import json
import logging
import boto3
from django.core.management.base import BaseCommand
from django.conf import settings
from botocore.client import ClientError
from storages.backends.s3boto3 import S3Boto3Storage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Will be executed with:
    ~~~
    python manage.py createbuckets
    ~~~
    """

    help = "Create static and media s3 buckets"

    public_read_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                "Resource": f"arn:aws:s3:::{settings.S3_STATIC_BUCKET_NAME}"
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{settings.S3_STATIC_BUCKET_NAME}/*"
            },
        ],
    }
    private_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PrivateBucketPolicy",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{settings.S3_MEDIA_BUCKET_NAME}/*"
            }
        ]
    }

    def handle(self, *args, **options):
        storage = S3Boto3Storage()
        s3_client = storage.connection

        # Static bucket creation
        try:
            s3_client.meta.client.head_bucket(
                Bucket=settings.S3_STATIC_BUCKET_NAME)
            print(f"{settings.S3_STATIC_BUCKET_NAME} already created")
        except ClientError:
            s3_client.create_bucket(
                Bucket=settings.S3_STATIC_BUCKET_NAME)
            # Apply public policy
            boto3.client(
                's3',
                aws_access_key_id=settings.S3_STORAGE_ACCESS_KEY,
                aws_secret_access_key=settings.S3_STORAGE_SECRET_KEY,
                endpoint_url=settings.S3_URL
            ).put_bucket_policy(
                Bucket=settings.S3_STATIC_BUCKET_NAME,
                Policy=json.dumps(self.public_read_policy)
            )
            print(f"{settings.S3_STATIC_BUCKET_NAME} succesfully created")

        # Media bucket creation
        try:
            s3_client.meta.client.head_bucket(
                Bucket=settings.S3_MEDIA_BUCKET_NAME)
            print(f"{settings.S3_MEDIA_BUCKET_NAME} already created")
        except ClientError:
            s3_client.create_bucket(
                Bucket=settings.S3_MEDIA_BUCKET_NAME)
            # Apply private policy
            boto3.client(
                's3',
                aws_access_key_id=settings.S3_STORAGE_ACCESS_KEY,
                aws_secret_access_key=settings.S3_STORAGE_SECRET_KEY,
                endpoint_url=settings.S3_URL
            ).put_bucket_policy(
                Bucket=settings.S3_MEDIA_BUCKET_NAME,
                Policy=json.dumps(self.private_policy)
            )
            print(f"{settings.S3_MEDIA_BUCKET_NAME} succesfully created")
