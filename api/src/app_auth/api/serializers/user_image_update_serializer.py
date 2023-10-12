"""
Provide serializer classes.
"""
import io
from rest_framework import serializers
from django.core.files.uploadedfile import TemporaryUploadedFile
from app_auth.models.user_model import User
import piexif
from PIL import Image


class UserImageUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to update user image
    """

    class Meta:  # pylint: disable=missing-class-docstring too-few-public-methods
        model = User
        fields = [
            "image",
        ]

    def validate_image(self, image: TemporaryUploadedFile):
        """
        Validate image param.
        """
        pil_image = Image.open(image)

        exif_data = piexif.load(pil_image.info['exif'])

        # Remove EXIF metadata
        orientation = exif_data['0th'].get(piexif.ImageIFD.Orientation)
        exif_data['0th'] = {}
        if orientation:
            exif_data['0th'][piexif.ImageIFD.Orientation] = orientation
        exif_data['Exif'] = {}
        exif_data['GPS'] = {}

        exif_bytes = piexif.dump(exif_data)

        new_image = io.BytesIO()
        pil_image.save(
            new_image,
            format=pil_image.format,
            exif=exif_bytes
        )
        new_image.seek(0)
        image.file = new_image

        return image
