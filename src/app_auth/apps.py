import logging
from django.apps import AppConfig


logger = logging.getLogger(__name__)


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.app_auth"
