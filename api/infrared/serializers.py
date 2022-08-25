from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.images import ImageFile

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
    """Used to validate query params and image resizing using sorl-thumbnal"""

    width = serializers.IntegerField()
    height = serializers.IntegerField()
    crop = serializers.CharField()

    def __init__(self, data: dict, *args, **kwargs):
        params = {key: value for key, value in data.items() if key in self.get_fields()}
        super().__init__(data=params, *args, **kwargs)

    def resize_image(self, image: ImageFieldFile) -> ImageFile:
        data = self.data
        width, height, crop = [data[key] for key in ["width", "height", "crop"]]
        width, height = min(width, image.width), min(height, image.height)

        return get_thumbnail(
            image,
            f"{width}x{height}",
            crop=crop,
            quality=settings.IMAGE_QUALITY,
        )
