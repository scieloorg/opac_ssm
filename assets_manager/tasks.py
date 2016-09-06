#coding: utf-8

import os
import logging

from django.core.files import File

from opac_ssm.taskapp.celery import app
from . import models

logger = logging.getLogger(__name__)

@app.task(bind=True)
def add_asset(self, file, type=None, origin=None, license=None, visibility=None,
              metadata=None, description=None):
    """
    Task to create a new asset.

    The only field mandatory is field file

    Params:
        :param file: can be File Like Object or a path (mandatory)
        :param type: is the type of asset ()
        :param origin: (model set default = 'WEBUP')
        :param license: (model set default = 'C')
        :param visibility: options: ['PRIVATE',
                                     'INTERNAL',
                                     'PUBLIC',] (model set default = 'INTERNAL')
        :param metadata: JSON with metadada about asset
        :param description: notes about asset
    """

    # Check if is a path
    if isinstance(file, basestring):
        try:
            fp = open(file)
        except IOError as e:
            logger.info(u"Error: %s" % e)
            raise

    # Check is a file like object
    if hasattr(file, 'read'):
        fp = file

    asset = models.Asset()
    filename = os.path.basename(getattr(fp, 'name', None))
    asset.file = File(fp, filename)
    asset.type = type

    if origin:
        asset.origin = origin
    else:
        asset.origin = 'OTHER'

    if license:
        asset.license = license

    if visibility:
        asset.visibility = visibility

    asset.metadata = metadata
    asset.description = description
    asset.save()

    logger.info(u"Successfully created asset with the id=%s, size=%s and path=%s" % (asset.id, asset.file.size, asset.file.path))
