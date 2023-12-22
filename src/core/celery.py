import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

import configurations

configurations.setup()

app = Celery("src.core")
app.config_from_object("django.conf:src.core.settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
