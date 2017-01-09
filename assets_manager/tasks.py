# -*- coding: utf-8 -*-

import io
import logging

from django.core.files import File

from opac_ssm.taskapp.celery import app
from . import models

logger = logging.getLogger(__name__)


@app.task(bind=True)
def add_asset(self, file, filename, type=None, metadata=None):
    """
    Task to create a new asset.

    The only field mandatory is field file

    Params:
        :param file: Bytes (Mandatory)
        :param filename: Name of file (Mandatory)
        :param type: is the type of asset
        :param metadata: JSON with metadada about asset
    """

    try:
        fp = io.BytesIO(file)
    except TypeError as e:
        logger.error(e)
        raise

    asset = models.Asset()
    asset.file = File(fp, filename)
    asset.type = type
    asset.metadata = metadata
    asset.save()

    logger.info(u"Successfully created asset with the id=%s, size=%s and path=%s",
                asset.id, asset.file.size, asset.file.path)

    return self.request.id
