from django.contrib import admin
from . import models


@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'type', 'origin', 'file', 'license',
        'created_at', 'created_by')
    readonly_fields = ('metadata', 'filename')
