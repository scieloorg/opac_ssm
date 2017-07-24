# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'bucket',
        'type',
        'file',
        'created_at',
        'updated_at'
    )
    readonly_fields = ('checksum', 'metadata', 'filename', 'uuid')
    list_filter = ('type', 'created_at', 'updated_at')
    search_fields = ['checksum', 'uuid', 'filename', 'bucket__name', 'metadata']


@admin.register(models.AssetBucket)
class AssetBucketAdmin(admin.ModelAdmin):
    list_display = ('name',)
