# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'type', 'file', 'created_at')
    readonly_fields = ('metadata', 'filename', 'task_id')

@admin.register(models.AssetBucket)
class AssetBucketAdmin(admin.ModelAdmin):
    list_display = ('name', )
