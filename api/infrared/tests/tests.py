import pytest
import rest_framework.status as status
from django.conf import settings
from PIL import Image
from rest_framework.test import APIClient
from sorl.thumbnail import delete

from infrared.models import ImageUpload
from infrared.serializers import ResizeParamSerializer

client = APIClient()


def get_resize_url(pk, width=100, height=100, crop="center"):
    return f"/api/v1/images/{pk}/resize/?width={width}&height={height}&crop={crop}"


@pytest.mark.django_db
def test_image_upload(test_image):
    res = client.post("/api/v1/images/", data={"image": test_image})

    assert res.status_code == status.HTTP_201_CREATED
    assert ImageUpload.objects.count() == 1

    data = res.json()
    assert not {"id", "image"} ^ data.keys()
    assert data["id"] and data["image"]

    delete(ImageUpload.objects.first().image)


@pytest.mark.django_db
def test_resize_image(test_image, image_upload_factory):
    width, height, crop = 100, 100, "center"
    params = {"width": width, "height": height, "crop": crop}

    serializer = ResizeParamSerializer(data=params)
    serializer.is_valid()

    image_upload = image_upload_factory(test_image)
    resized_image = serializer.resize_image(image_upload.image)

    # BASE_DIR / path does not work properly for some reason
    file_path = str(settings.BASE_DIR) + "/" + resized_image.url
    with Image.open(file_path) as image:
        assert (width, height) == image.size

    delete(image_upload.image)


@pytest.mark.django_db
def test_view_resize(test_image, image_upload_factory):
    width, height = 100, 100
    image_upload = image_upload_factory(test_image)

    url = get_resize_url(image_upload.pk, width=width, height=height)
    res = client.put(url)

    assert res.status_code == status.HTTP_200_OK
    assert "image" in res.json()

    data = res.json()
    file_path = str(settings.BASE_DIR) + "/" + data["image"]
    with Image.open(file_path) as resized_image:
        assert (width, height) == resized_image.size

    delete(image_upload.image)


@pytest.mark.django_db
def test_view_resize_invalid_crop(test_image, image_upload_factory):
    image_upload = image_upload_factory(test_image)

    url = get_resize_url(image_upload.pk, crop="invalid_crop")
    res = client.put(url)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in res.json()

    delete(image_upload.image)


@pytest.mark.django_db
def test_view_resize_invalid_params(test_image, image_upload_factory):
    image_upload = image_upload_factory(test_image)

    url = get_resize_url(image_upload.pk, width="invalid_width")
    res = client.put(url)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "width" in res.json()

    delete(image_upload.image)
