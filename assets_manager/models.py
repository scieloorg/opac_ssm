from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


ASSET_LICENSE_CHOICES = [
    ('CC-BY', _('Createive Commons')),
    ('GPL', _('GPL')),
    ('BSD', _('BSD')),
    ('MIT', _('MIT')),
    ('C', _('Copyright'))
]

ASSET_VISIBILITY_CHOICES = [
    ('PRIVATE', _('Private')),
    ('INTERNAL', _('Internal')),
    ('PUBLIC', _('Public'))
]

ASSET_ORIGIN_CHOICES = [
    ('WEBUP', _('Web Upload')),
    ('FTP', _('FTP')),
    ('OTHER', _('Other'))
]


def upload_to_path(instance, filename):
    return 'assets/raw/{0}/{1}'.format(
        instance.origin, filename)


class Asset(models.Model):
    """
    Class that represent Asset.
    """

    type = models.CharField(max_length=32, null=True, blank=True)
    file = models.FileField(upload_to=upload_to_path, max_length=500)
    filename = models.CharField(max_length=128, null=True, blank=True)

    origin = models.CharField(
        choices=ASSET_ORIGIN_CHOICES,
        max_length=20, default="WEBUP")
    license = models.CharField(
        choices=ASSET_LICENSE_CHOICES, max_length=20,
        null=True, blank=True, default='C')

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assets_created',
        null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assets_updated',
        null=True, blank=True)

    owned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assets_owned',
        null=True, blank=True)
    owned_at = models.DateTimeField(null=True, blank=True)

    visibility = models.CharField(
        choices=ASSET_VISIBILITY_CHOICES,
        max_length=20, default="INTERNAL")

    metadata = JSONField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.file)

    class Meta:
        verbose_name = u"Asset"
        verbose_name_plural = u"Assets"
        ordering = ['-created_at']
