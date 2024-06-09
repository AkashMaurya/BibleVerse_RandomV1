from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePage, name="homepage"),
    path("generate/", views.generate_image, name="generate_image"),
    path("download/", views.download_image_view, name="download_image"),
]
