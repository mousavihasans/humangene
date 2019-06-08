from django.contrib import admin
from django.contrib.admin.decorators import register
from customersupport.models import TrackTask


@register(TrackTask)
class TrackTasksAdmin(admin.ModelAdmin):
    pass