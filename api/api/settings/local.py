from pathlib import Path

from api.settings.base import *  # noqa
from api.settings.base import BASE_DIR  # noqa

STATIC_URL = "static/"
STATICFILES_DIRS: list[Path | str] = []

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
