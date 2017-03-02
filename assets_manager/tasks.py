# -*- coding: utf-8 -*-

import io
import json
import logging

from django.core.files import File

from opac_ssm.taskapp.celery import app
from . import models

logger = logging.getLogger(__name__)


@app.task(bind=True)
def add_bucket(self, bucket_name):
    """
    Task to create a new bucket.

    Params:
        :param bucket_name: String (Mandatory)

    Return a boolean True if this a new bucket and False means already exists
    """

    bucket, created = models.AssetBucket.objects.get_or_create(name=bucket_name)

    return (bucket, created)


@app.task(bind=True)
def update_bucket(self, bucket_name, new_name):
    """
    Task to update the bucket by name.

    Params:
        :param bucket_name: String (Mandatory) Case Insensitive
        :param new_name: String (Mandatory)

    Return a tuple with (success(boolean), old_name, new_name)
    """

    success = False

    try:
        ori_exists = models.AssetBucket.objects.filter(name__iexact=bucket_name).exists()
        des_exists = models.AssetBucket.objects.filter(name__iexact=new_name).exists()

        if ori_exists and not des_exists:
            ori_bucket = models.AssetBucket.objects.get(name__iexact=bucket_name)
            ori_bucket.name = new_name
            ori_bucket.save()
            success = True
        elif ori_exists and des_exists:
            logger.error(u"Existe um bucket com o nome: %s", new_name)
            raise
        elif not ori_exists:
            logger.error(u"Não existe um bucket com o nome: %s", bucket_name)
            raise

    except models.AssetBucket.DoesNotExist as e:
        logger.error(e)
        raise

    return (success, bucket_name, new_name)


@app.task(bind=True)
def remove_bucket(self, bucket_name):
    """
    Task to remove bucket by name.

    Params:
        :param bucket_name: String (Mandatory) Case Insensitive

    Attention: The Django.delete() function by default it emulates the behavior
    of the SQL constraint ON DELETE CASCADE – in other words, any objects which
    had foreign keys pointing at the object to be deleted will be deleted along
    with it

    Return value describing the number of objects deleted, if it does not exists
    return a tuple with (0, {}).

    More about delete method:
    https://docs.djangoproject.com/en/1.10/topics/db/queries/#deleting-objects
    """
    result = (0, {})

    try:
        result = models.AssetBucket.objects.get(name__iexact=bucket_name).delete()
        logger.info(u"Bucket %s removido com sucesso.", bucket_name)
    except models.AssetBucket.DoesNotExist as e:
        logger.error(e)
        raise

    return result


@app.task(bind=True)
def exists_bucket(self, bucket_name):
    """
    Task to check if exists a bucket by name.

    Params:
        :param bucket_name: String (Mandatory) Case Insensitive

    Return a boolean
    """
    return models.AssetBucket.objects.filter(name__iexact=bucket_name).exists()


@app.task(bind=True)
def add_asset(self, file, filename, type=None, metadata=None, bucket_name=""):
    """
    Task to create a new asset.

    Mandatory fields are file and filename

    Params:
        :param file: Bytes (Mandatory)
        :param filename: Name of file (Mandatory)
        :param type: is the type of asset
        :param metadata: JSON with metadada about asset
        :param bucket_name: Name of bucket related to asset

    Return the task uuid
    """

    try:
        fp = io.BytesIO(file)
    except TypeError as e:
        logger.error(e)
        raise

    if bucket_name == "":
        bucket_name = "UNKNOW"

    bucket, created = add_bucket(bucket_name)

    if created:
        logger.info(u"Novo bucket adicionado com o nome: %s", bucket.name)

    asset = models.Asset()
    asset.file = File(fp, filename)
    asset.filename = filename
    asset.type = type
    asset.metadata = metadata
    asset.uuid = self.request.id # Save task id on uuid field.
    asset.bucket = bucket
    asset.save()

    logger.info(u"Criado ativo com sucesso id=%s, tamanho=%s bytes e caminho=%s",
                asset.id, asset.file.size, asset.file.path)

    return self.request.id


@app.task(bind=True)
def remove_asset(self, asset_uuid):
    """
    Task to remove asset by id.

    Params:
        :param asset_uuid: UUID (Mandatory)

    Attention: The Django.delete() function by default it emulates the behavior
    of the SQL constraint ON DELETE CASCADE – in other words, any objects which
    had foreign keys pointing at the object to be deleted will be deleted along
    with it

    Return value describing the number of objects deleted, if it does not exists
    return a tuple with (0, {}).

    """
    result = (0, {})

    try:
        result = models.Asset.objects.get(uuid=asset_uuid).delete()
        logger.info(u"Asset %s removido com sucesso.", asset_uuid)
    except models.Asset.DoesNotExist as e:
        logger.error(e)
        raise

    return result


@app.task(bind=True)
def update_asset(self, uuid, file=None, filename=None, type=None, metadata=None,
                 bucket_name=None):
    """
    Task to update asset.

    The only field mandatory is field uuid

    Params:
        :param file: Bytes
        :param filename: Name of file
        :param type: is the type of asset
        :param metadata: JSON with metadada about asset
        :param bucket_name: Name of bucket related to asset

    Return a JSON String with all atrib of asset, return {} if asset does not
    exists.
    """
    asset_dict = {}

    try:
        asset = models.Asset.objects.get(uuid=uuid)
    except models.Asset.DoesNotExist as e:
        logger.error(e)
        raise
    else:

        if file:
            try:
                fp = io.BytesIO(file)
                asset.file = File(fp, filename)
            except TypeError as e:
                logger.error(e)
                raise

        if bucket_name:
            bucket, created = add_bucket(bucket_name)
            asset.bucket = bucket

            if created:
                logger.info(u"Novo bucket adicionado com o nome: %s", bucket.name)

        if filename:
            asset.filename = filename

        if type:
            asset.type = type

        if metadata:
            asset.metadata = metadata

        asset.save()

        logger.info(u"Atualizado ativo com sucesso id=%s, tamanho=%s bytes e caminho=%s",
                    asset.id, asset.file.size, asset.file.path)

        asset_dict = dict(
            asset_type=asset.type, asset_file=str(asset.file),
            asset_filename=asset.filename, asset_uuid=str(asset.uuid),
            asset_created_at=asset.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            asset_update_at=asset.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            asset_meta=asset.metadata, asset_bucket=asset.bucket.name
            )

    return json.dumps(asset_dict)


@app.task(bind=True)
def exists_asset(self, asset_uuid):
    """
    Task to check if exists a asset by uuid.

    Params:
        :param asset_uuid: String (UUID)

    Return a boolean
    """
    return models.Asset.objects.filter(uuid=asset_uuid).exists()
