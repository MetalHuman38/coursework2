"""
This file contains all route and path configurations for the app.
"""

from django.urls import path
from . import views

app_name = "uidirectory"

urlpatterns = [
    path("", views.home, name="home"),
    path("uploadimg", views.upload_image, name="uploadimg"),
    path("classify_image", views.classify_image, name="classify_image"),
    path("feedback/", views.feedback, name="feedback"),
]
