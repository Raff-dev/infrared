from django.urls import include, path
from rest_framework.routers import DefaultRouter

from infrared.views import ImageViewset, index

router = DefaultRouter()
router.register("images", ImageViewset)


urlpatterns = [
    path("", index, name="index"),
    path("", include(router.urls)),
]
