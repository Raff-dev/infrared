import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from sorl.thumbnail.images import ImageFile

from infrared.models import ImageUpload

TEST_IMAGE_PATH = settings.BASE_DIR / "infrared/tests/resources/test.jpg"


@pytest.fixture
def test_image() -> ImageFile:
    """Creates Django image file for testing purposes"""
    with open(TEST_IMAGE_PATH, "rb") as file:
        return SimpleUploadedFile(
            file.name, content=file.read(), content_type="image/jpeg"
        )


@pytest.fixture
def image_upload_factory(db):
    def create_image_upload(image: ImageFile):
        return ImageUpload.objects.create(image=image)

    return create_image_upload
