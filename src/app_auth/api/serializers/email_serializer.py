"""
Provide serializer classes.
"""
from rest_framework import serializers


class EmailSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer to send email
    """

    email = serializers.EmailField(
        required=True
    )
