"""Admin configuration for the currency app."""

from django.contrib import admin

from .models import Currency

admin.site.register(Currency)
