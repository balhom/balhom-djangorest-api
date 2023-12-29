import os
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Will be executed with:
    ~~~
    python manage.py collectmedia
    ~~~
    """

    help = "Upload default stored media files to s3 bucket"

    def handle(self, *args, **options):
        for dirpath, _, filenames in os.walk(settings.MEDIA_ROOT):
            for file in filenames:
                if str(file).lower().endswith((".png", ".jpg", ".jpeg")):
                    filepath = os.path.join(dirpath, file)
                    object_name = str(filepath).removeprefix(
                        os.path.join(str(settings.MEDIA_ROOT), "")
                    )
                    print(f"Uploading {object_name}")
                    try:
                        with open(filepath, 'rb') as image_file:
                            default_storage.save(
                                object_name,
                                image_file
                            )
                    except Exception as err:
                        print(err)
