from pathlib import Path

from storages.backends.s3boto3 import S3Boto3Storage

from api.settings.base import *  # noqa
from api.settings.base import BASE_DIR, env

# sorl-thumbnail workaround for AWS S3 integration underperformance
THUMBNAIL_FORCE_OVERWRITE = True

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = "api.settings.storage.MediaStorage"

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS: list[Path] = []


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = True
