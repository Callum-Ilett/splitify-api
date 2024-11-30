"""URLs for the auth0authorization app."""

from django.urls import path

from . import views

urlpatterns = [
    path("api/public", views.public),
    path("api/private", views.private),
]
