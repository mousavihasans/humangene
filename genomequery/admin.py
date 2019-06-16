from django.contrib import admin
from django.contrib.admin.decorators import register
from genomequery.models import QueryItem, QueryTypeChoices, GenomeQuery


@register(GenomeQuery)
class GenomeQueryAdmin(admin.ModelAdmin):
    pass


@register(QueryItem)
class QueryItemAdmin(admin.ModelAdmin):
    list_display = ('performed_by', 'type', 'performed_at')
    readonly_fields = ('created_by', 'type', 'response')

    def save_model(self, request, instance, form, change):
        if instance.type == QueryTypeChoices.created_manually:
            instance.created_by = request.user
            super().save_model(request, instance, form, change)
