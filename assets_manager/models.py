# -*- coding: utf-8 -*-
import hashlib
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.postgres.fields import JSONField

from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver


class AssetBucket(models.Model):
    name = models.CharField('nome', max_length=256, unique=True,
                            default='UNKNOW')

    def __str__(self):
        return self.name


def upload_to_path(instance, filename):
    """
    Method to construct the path of asset.

    IMPORTANT: This path is dependent of bucket name, if bucket name doesnt
    exists, asset is save in ASSET_FOLDER.
    """
    if instance.bucket:
        return '{0}/{1}/{2}'.format(settings.ASSET_FOLDER,
                                    instance.bucket.name, filename)
    else:
        return '{0}/{1}'.format(settings.ASSET_FOLDER, filename)


class Asset(models.Model):
    """
    Class that represent Asset.
    """

    type = models.CharField(max_length=32, null=True, blank=True)
    file = models.FileField(upload_to=upload_to_path, max_length=500)
    filename = models.CharField(max_length=128, null=True, blank=True)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    metadata = JSONField(null=True, blank=True)

    bucket = models.ForeignKey(AssetBucket, null=True, blank=False)

    checksum = models.CharField(max_length=64, null=False, blank=False,
                                editable=False)

    def __unicode__(self):
        return self.file

    class Meta:
        verbose_name = u"Asset"
        verbose_name_plural = u"Assets"
        ordering = ['-created_at']

    @property
    def get_absolute_url(self):
        """
        Return path URL file
        """
        return "{0}{1}".format(settings.MEDIA_URL, self.file)

    @property
    def get_full_absolute_url(self):
        """
        Return full URL to file
        """
        domain = Site.objects.get_current().domain

        return "{0}{1}{2}".format(settings.ASSET_PROTOCOL_PREFIX,
                                  domain, self.get_absolute_url)


@receiver(pre_delete, sender=Asset)
def asset_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(False)


@receiver(pre_save, sender=Asset)
def generate_checksum(sender, instance, *args, **kwargs):
    """
    Generate checksum before save asset.
    """
    text = instance.file.read()

    instance.checksum = hashlib.sha256(text).hexdigest()
