import os
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from minio import Minio

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Will be executed with:
    ~~~
    python manage.py collectmedia
    ~~~
    """

    help = "Upload default stored media files to minio bucket"

    def handle(self, *args, **options):
        minio_client = Minio(
            endpoint=settings.S3_STORAGE_ENDPOINT,
            access_key=settings.S3_STORAGE_ACCESS_KEY,
            secret_key=settings.S3_STORAGE_SECRET_KEY,
            secure="https" in settings.S3_URL,
        )
        for dirpath, _, filenames in os.walk(settings.MEDIA_ROOT):
            for file in filenames:
                if str(file).lower().endswith((".png", ".jpg", ".jpeg")):
                    filepath = os.path.join(dirpath, file)
                    object_name = str(filepath).removeprefix(
                        os.path.join(str(settings.MEDIA_ROOT), "")
                    )
                    print(f"Uploading {object_name}")
                    try:
                        minio_client.fput_object(
                            bucket_name=settings.S3_MEDIA_BUCKET_NAME,
                            object_name=object_name,
                            file_path=filepath,
                        )
                    except Exception as err:
                        print(err)
