"""
Provide serializer classes.
"""
from rest_framework import serializers


class CredentialsSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer to get access tokens
    """

    email = serializers.EmailField(
        required=True
    )
    password = serializers.CharField(
        required=True,
    )
