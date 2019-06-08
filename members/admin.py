from django.contrib import admin
from django.contrib.admin.decorators import register

from members.models import Profile


@register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass