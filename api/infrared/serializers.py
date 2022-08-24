from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from infrared.models import ImageUpload


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ["id", "image"]

    def create(self, validated_data: dict):
        image_upload = super().create(validated_data)
        return image_upload


class ImageResponseSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ResizeParamSerializer(serializers.Serializer):
    """Used to validate query params and image resizing using sorl.thumbnal"""

    width = serializers.IntegerField()
    height = serializers.IntegerField()
    crop = serializers.CharField()

    def __init__(self, data, *args, **kwargs):
        params = {key: value for key, value in data.items() if key in self.get_fields()}
        return super().__init__(data=params, *args, **kwargs)

    def resize_image(self, image: ImageFieldFile):
        data = self.data
        width, height, crop = data["width"], data["height"], data["crop"]

        return get_thumbnail(
            image,
            f"{width}x{height}",
            crop=crop,
            quality=settings.IMAGE_QUALITY,
        )
