from django.urls import path

from infrared import views

urlpatterns = [
    path("", views.index, name="index"),
]
