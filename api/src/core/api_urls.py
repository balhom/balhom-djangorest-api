from django.urls import path, include
from app_auth.api import urls as auth_urls
from balance.api import urls as balance_urls
from version.api import urls as version_urls
from app_statistics.api import urls as statistics_urls

urlpatterns = [
    # Auth app urls:
    path("", include(auth_urls)),
    # Balance app urls:
    path("", include(balance_urls)),
    # Version app urls:
    path("", include(version_urls)),
    # Statistics app urls:
    path("", include(statistics_urls)),
]
