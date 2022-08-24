import pytest
import rest_framework.status as status
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from infrared.models import ImageUpload

TEST_IMAGE_PATH = settings.BASE_DIR / "infrared/tests/resources/test.jpg"

client = APIClient()


@pytest.fixture
def test_image():
    """Creates Django image file for testing purposes"""
    with open(TEST_IMAGE_PATH, "rb") as file:
        return SimpleUploadedFile(
            file.name, content=file.read(), content_type="image/jpeg"
        )


@pytest.mark.django_db
def test_image_upload(test_image):
    res = client.post("/api/v1/images/", data={"image": test_image})

    assert res.status_code == status.HTTP_201_CREATED
    assert ImageUpload.objects.count() == 1

    data = res.json()
    assert not {"id", "image"} ^ data.keys()
    assert data["id"] and data["image"]
