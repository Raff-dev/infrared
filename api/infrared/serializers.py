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


class ImageResponseSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ResizeParamSerializer(serializers.Serializer):
    """Used to validate query params and image resizing using sorl-thumbnal"""

    width = serializers.IntegerField()
    height = serializers.IntegerField()
    crop = serializers.CharField()

    def __init__(self, data: dict | None = None, *args, **kwargs):
        if data:
            data = {key: data.get(key) for key in self.get_fields()}
        super().__init__(data=data, *args, **kwargs)

    def resize_image(self, image: ImageFieldFile) -> ImageFile:
        width, height, crop = [self.data[key] for key in ["width", "height", "crop"]]
        width, height = min(width, image.width), min(height, image.height)

        return get_thumbnail(
            image,
            f"{width}x{height}",
            crop=crop,
            quality=settings.IMAGE_QUALITY,
        )
