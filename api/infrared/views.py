from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import parsers, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from sorl.thumbnail.parsers import ThumbnailParseError

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
    parser_classes = (
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_id="Upload Image",
        operation_description="Upload base image used for future resizing.",
        request_body=ImageUploadSerializer,
        responses={
            201: ImageUploadSerializer,
            400: openapi.Response("Bad Request"),
        },
    )
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    # although indepotent, this method might create resources,
    # therefore should not be a GET
    @action(detail=True, methods=["PUT"])
    @swagger_auto_schema(
        operation_id="Resize Image",
        query_serializer=ResizeParamSerializer,
        operation_description="""
        Resizes images via sorl-thumbnail and returns image url inside the response.

        Resort to documentation below for cropping and resizing options:
        https://sorl-thumbnail.readthedocs.io/en/latest/template.html#crop
        """,
        request_body=no_body,
        responses={
            200: ImageResponseSerializer,
            400: openapi.Response("Bad Request"),
        },
    )
    def resize(self, request: Request, **kwargs) -> Response:
        """Expects width: int, height: int, crop: string as URL parameters."""
        image_upload: ImageUpload = self.get_object()
        params = request.query_params.dict()

        serializer = ResizeParamSerializer(data=params)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        try:
            resized_image = serializer.resize_image(image_upload.image)
            serializer = ImageResponseSerializer(
                data={"image": resized_image},
                # add context to return full url on local
                context={"request": request},
            )
            serializer.is_valid()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except ThumbnailParseError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(e)},
            )
