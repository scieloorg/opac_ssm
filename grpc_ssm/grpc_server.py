#!/usr/bin/env python

import time
import logging
import json
from concurrent import futures

import grpc
from grpc_ssm import opac_pb2
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

from celery.result import AsyncResult

from assets_manager import tasks
from assets_manager import models

DEFAULT_MAX_RECEIVE_MESSAGE_LENGTH = 90 * 1024 * 1024
DEFAULT_MAX_SEND_MESSAGE_LENGTH = 90 * 1024 * 1024


class Asset(opac_pb2.AssetServiceServicer):

    def add_asset(self, request, context):
        """
        Return a task id
        """
        task_result = tasks.add_asset.delay(request.file, request.filename,
                                            request.type, request.metadata,
                                            request.bucket)

        return opac_pb2.TaskId(id=task_result.id)

    def get_asset(self, request, context):
        """
        Return an Asset or message erro when asset doesnt exists
        """
        try:
            asset = models.Asset.objects.get(uuid=request.id)
        except models.Asset.DoesNotExist as e:
            logging.error(str(e))
            context.set_details(str(e))
            raise
        else:
            try:
                fp = open(asset.file.path, 'rb')
            except IOError as e:
                logging.error(e)
                context.set_details(e)
                raise

            return opac_pb2.Asset(file=fp.read(),
                                  filename=asset.filename,
                                  type=asset.type,
                                  metadata=json.dumps(asset.metadata),
                                  uuid=asset.uuid.hex,
                                  bucket=asset.bucket.name,
                                  checksum=asset.checksum,
                                  absolute_url=asset.get_absolute_url,
                                  full_absolute_url=asset.get_full_absolute_url,
                                  created_at=asset.created_at.isoformat(),
                                  updated_at=asset.updated_at.isoformat())

    def update_asset(self, request, context):
        """
        Return a task id
        """

        task_result = tasks.update_asset.delay(request.uuid, request.file,
                                               request.filename, request.type,
                                               request.metadata, request.bucket)

        return opac_pb2.TaskId(id=task_result.id)

    def remove_asset(self, request, context):
        """
        Return a AssetExists
        """

        result = tasks.remove_asset(asset_uuid=request.id)

        return opac_pb2.AssetRemoved(exist=result)

    def exists_asset(self, request, context):
        """
        Return a AssetExists
        """

        result = tasks.exists_asset(asset_uuid=request.id)

        return opac_pb2.AssetExists(exist=result)

    def get_task_state(self, request, context):
        """
        Return an Asset state
        """
        res = AsyncResult(request.id)

        return opac_pb2.TaskState(state=res.state)

    def get_asset_info(self, request, context):
        """
        Return an Asset info
        """
        try:
            asset = models.Asset.objects.get(uuid=request.id)
        except models.Asset.DoesNotExist as e:
            logging.error(str(e))
            context.set_details(str(e))
            raise
        else:
            return opac_pb2.AssetInfo(url=asset.get_full_absolute_url,
                                      url_path=asset.get_absolute_url)

    def get_bucket(self, request, context):
        """
        Return a bucket of any asset
        """
        try:
            asset = models.Asset.objects.get(uuid=request.id)
        except models.Asset.DoesNotExist as e:
            logging.error(str(e))
            context.set_details(str(e))
            raise
        else:
            return opac_pb2.Bucket(name=asset.bucket.name)

    def query(self, request, context):
        """
        Return a list of assets if it exists
        """
        asset_list = []

        assets = opac_pb2.Assets()

        filters = {}

        if request.checksum:
            filters['checksum'] = request.checksum

        if request.filename:
            filters['filename'] = request.filename

        if request.type:
            filters['type'] = request.type

        if request.uuid:
            filters['uuid'] = request.uuid

        if request.bucket:
            filters['bucket'] = request.bucket

        result = tasks.query(filters, metadata=request.metadata)

        for ret in result:
            asset = opac_pb2.Asset()
            asset.filename = ret.filename
            asset.type = ret.type
            asset.metadata = json.dumps(ret.metadata)
            asset.uuid = ret.uuid.hex
            asset.checksum = ret.checksum
            asset.bucket = ret.bucket.name
            asset.absolute_url = ret.get_absolute_url
            asset.full_absolute_url = ret.get_full_absolute_url
            asset.created_at = ret.created_at.isoformat()
            asset.updated_at = ret.updated_at.isoformat()

            asset_list.append(asset)

        assets.assets.extend(asset_list)

        return assets


class AssetBucket(opac_pb2.BucketServiceServicer):

    def add_bucket(self, request, context):
        """
        Return a task id
        """
        task_result = tasks.add_bucket.delay(bucket_name=request.name)

        return opac_pb2.TaskId(id=task_result.id)

    def update_bucket(self, request, context):
        """
        Return a task id
        """
        task_result = tasks.update_bucket.delay(bucket_name=request.name,
                                                new_name=request.new_name)

        return opac_pb2.TaskId(id=task_result.id)

    def remove_bucket(self, request, context):
        """
        Return a BucketRemoved
        """

        result = tasks.remove_bucket(bucket_name=request.name)

        return opac_pb2.BucketRemoved(exist=result)

    def exists_bucket(self, request, context):
        """
        Return a AssetExists
        """

        result = tasks.exists_bucket(bucket_name=request.name)

        return opac_pb2.BucketExists(exist=result)

    def get_task_state(self, request, context):
        """
        Return an Asset state
        """
        res = AsyncResult(request.id)

        return opac_pb2.TaskState(state=res.state)

    def get_assets(self, request, context):
        """
        Return a list of assets
        """
        asset_list = []

        # Necessário retornar um objeto to tipo Assets
        assets = opac_pb2.Assets()

        result = models.Asset.objects.filter(bucket__name=request.name)

        for ret in result:
            asset = opac_pb2.Asset()
            asset.file = ret.file.read()
            asset.filename = ret.filename
            asset.type = ret.type
            asset.metadata = json.dumps(ret.metadata)
            asset.uuid = ret.uuid.hex
            asset.checksum = ret.checksum
            asset.bucket = ret.bucket.name
            asset.absolute_url = ret.get_absolute_url
            asset.full_absolute_url = ret.get_full_absolute_url
            asset.created_at = ret.created_at.isoformat()
            asset.updated_at = ret.updated_at.isoformat()

            asset_list.append(asset)

        assets.assets.extend(asset_list)

        return assets


def serve(host='[::]', port=5000, max_workers=4,
          max_receive_message_length=None,
          max_send_message_length=None):

    if max_receive_message_length is None:
        max_receive_message_length = DEFAULT_MAX_RECEIVE_MESSAGE_LENGTH

    if max_send_message_length is None:
        max_send_message_length = DEFAULT_MAX_SEND_MESSAGE_LENGTH

    servicer = health.HealthServicer()

    servicer.set('', health_pb2.HealthCheckResponse.SERVING)

    # Asset
    servicer.set('get_asset', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('add_asset', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('update_asset', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('remove_asset', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('exists_asset', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('get_asset_info', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('get_task_state', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('get_bucket', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('query', health_pb2.HealthCheckResponse.SERVING)

    # Bucket
    servicer.set('add_bucket', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('update_bucket', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('remove_bucket', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('exists_bucket', health_pb2.HealthCheckResponse.SERVING)
    servicer.set('get_assets', health_pb2.HealthCheckResponse.SERVING)

    options = [
        ('grpc.max_receive_message_length', max_receive_message_length),
        ('grpc.max_send_message_length', max_send_message_length)
    ]
    logging.info('Starting GRPC server with this options: %s', options)

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=options)

    opac_pb2.add_AssetServiceServicer_to_server(Asset(), server)
    opac_pb2.add_BucketServiceServicer_to_server(AssetBucket(), server)

    # Health service
    health_pb2_grpc.add_HealthServicer_to_server(servicer, server)

    # Set port and Start Server
    server.add_insecure_port('{0}:{1}'.format(host, port))
    logging.info('Started GRPC server on host: {0}, port: {1}, accept connections!'.format(host, port))
    server.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info('User stopping server...')
        server.stop(0)
        logging.info('Server stopped; exiting.')
    except Exception as e:
        logging.info('Caught exception "%s"; stopping server...', e)
        server.stop(0)
        logging.info('Server stopped; exiting.')


if __name__ == '__main__':
    serve()
