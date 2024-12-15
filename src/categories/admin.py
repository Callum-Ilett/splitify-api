"""Admin for the categories app."""

from django.contrib import admin

from categories.models import Category

admin.site.register(Category)
