#!/usr/bin/env python

import time
import logging
from concurrent import futures

import grpc
from grpc_ssm import opac_pb2

from celery.result import AsyncResult

from assets_manager import tasks
from assets_manager import models

logger = logging.getLogger(__name__)

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
        Return an Asset
        """
        try:
            asset = models.Asset.objects.get(uuid=request.id)
        except models.Asset.DoesNotExist as e:
            logger.error(e)
            raise
        else:

            try:
                fp = open(asset.file.path, 'rb')
            except IOError as e:
                logger.error(e)
                raise

            return opac_pb2.Asset(file=fp.read(), filename=asset.filename,
                                  type=asset.type, metadata=asset.metadata,
                                  uuid=str(asset.uuid), bucket=asset.bucket.name)

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
        Return a task id
        """

        task_result = tasks.remove_asset.delay(asset_uuid=request.id)

        return opac_pb2.TaskId(id=task_result.id)

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
            logger.error(e)
            raise
        else:
            return opac_pb2.AssetInfo(url=asset.get_full_absolute_url,
                                      url_path=asset.get_absolute_url)


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
        Return a task id
        """

        task_result = tasks.remove_bucket.delay(bucket_name=request.name)

        return opac_pb2.TaskId(id=task_result.id)

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


def serve(host='[::]', port=5000, max_workers=4):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    opac_pb2.add_AssetServiceServicer_to_server(Asset(), server)
    opac_pb2.add_BucketServiceServicer_to_server(AssetBucket(), server)
    server.add_insecure_port('{0}:{1}'.format(host, port))
    server.start()

    print('Started GRPC server on localhost, port: {0}, accept connections!'.format(port))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
