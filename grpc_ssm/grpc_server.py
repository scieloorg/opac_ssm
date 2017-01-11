#!/usr/bin/env python

import time
import logging
from concurrent import futures

import grpc
from grpc_ssm import opac_pb2

# from django.core.exceptions import ObjectDoesNotExist
from celery.result import AsyncResult

from assets_manager import tasks
from assets_manager import models

logger = logging.getLogger(__name__)

class Asset(opac_pb2.AssetServiceServicer):

    def add_asset(self, request, context):
        """
        Return a Asset object
        """
        task_result = tasks.add_asset.delay(request.file, request.filename,
                                            request.type, request.metadata)

        return opac_pb2.TaskId(id=task_result.id)

    def get_task_state(self, request, context):
        """
        Return a Asset state
        """
        res = AsyncResult(request.id)

        return opac_pb2.TaskState(state=res.state)

    def get_asset_info(self, request, context):
        """
        Return a Asset info
        """
        try:
            asset = models.Asset.objects.get(task_id=request.id)
        except models.Asset.DoesNotExist as e:
            logger.error(e)
            raise
        else:
            return opac_pb2.AssetInfo(url=asset.get_full_absolute_url,
                                      url_path=asset.get_absolute_url)


def serve(port=5000, max_workers=4):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    opac_pb2.add_AssetServiceServicer_to_server(Asset(), server)
    server.add_insecure_port('[::]:{0}'.format(port))
    server.start()

    print('Started GRPC server on localhost, port: {0}, accept connections!'.format(port))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
