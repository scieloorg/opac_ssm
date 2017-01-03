from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


def upload_to_path(instance, filename):
    return 'assets/raw/{0}/'.format(filename)


class Asset(models.Model):
    """
    Class that represent Asset.
    """

    type = models.CharField(max_length=32, null=True, blank=True)
    file = models.FileField(upload_to=upload_to_path, max_length=500)
    filename = models.CharField(max_length=128, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    metadata = JSONField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.file)

    class Meta:
        verbose_name = u"Asset"
        verbose_name_plural = u"Assets"
        ordering = ['-created_at']
