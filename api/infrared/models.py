from django.db import models
from django.utils.translation import gettext_lazy as _

IMAGES_PATH = "images"


class ImageUpload(models.Model):
    image = models.ImageField(_("image"), upload_to=IMAGES_PATH)
