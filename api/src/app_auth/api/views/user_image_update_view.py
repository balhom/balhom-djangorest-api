"""
Provide view classes.
"""
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from django.utils.translation import gettext_lazy as _
from core.permissions import IsCurrentVerifiedUser
from app_auth.models.user_model import User
from app_auth.api.serializers.user_image_update_serializer import (
    UserImageUpdateSerializer,
)


class UserImageUpdateView(generics.UpdateAPIView):
    """
    View for User image update
    """

    queryset = User.objects.all()
    permission_classes = (IsCurrentVerifiedUser,)
    serializer_class = UserImageUpdateSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self, queryset=None):  # pylint: disable=unused-argument
        return self.request.user
