"""Admin configuration for the groups app."""

from django.contrib import admin

from .models import Group, GroupMember


class GroupMemberInline(admin.TabularInline):
    """Group member inline."""

    model = GroupMember


class GroupAdmin(admin.ModelAdmin):
    """Group admin."""

    inlines = [GroupMemberInline]


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMember)
