from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class VersionView(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60))
    def get(self, request, format=None):  # pylint: disable=unused-argument redefined-builtin
        """
        This view will be cached for 60 seconds
        """
        return Response(
            data={
                "app_version": settings.APP_VERSION,
                "web_version": settings.WEB_VERSION,
                "api_version": settings.API_VERSION
            }
        )
