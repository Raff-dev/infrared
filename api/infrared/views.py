from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from infrared.models import ImageUpload
from infrared.serializers import (
    ImageResponseSerializer,
    ImageUploadSerializer,
    ResizeParamSerializer,
)


def index(request):
    return JsonResponse({"Hello": "world!"})


class ImageViewset(CreateModelMixin, GenericViewSet):
    serializer_class = ImageUploadSerializer
    queryset = ImageUpload.objects.all()

    # although indepotent, this method can create resources in the database,
    # therefore should not be a GET
    @action(detail=True, methods=["GET"])
    def resize(self, request: Request, **kwargs) -> Response:
        """
        Takes width: int, height: int, crop: string URL parameters.
        """
        image_upload = self.get_object()
        params = request.query_params.dict()

        serializer = ResizeParamSerializer(data=params)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        resized_image = serializer.resize_image(image_upload.image)
        serializer = ImageResponseSerializer(data={"image": resized_image})
        serializer.is_valid()

        return Response(status=status.HTTP_200_OK, data=serializer.data)
