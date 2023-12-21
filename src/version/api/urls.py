from django.urls import path
from src.version.api.views import VersionView

urlpatterns = [
    path("version", VersionView.as_view(),
         name="version_get")
]
