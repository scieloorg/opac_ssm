#!/usr/bin/env python

import time
from concurrent import futures

import grpc
from grpc_ssm import opac_pb2

from assets_manager import tasks


class Asset(opac_pb2.AssetServiceServicer):

    def add_asset(self, request, context):
        """
        Return a Asset object
        """

        file = request.file
        filename = request.filename
        filetype = request.type
        metadata = request.metadata

        tasks.add_asset.delay(file, filename, filetype, metadata)

        return opac_pb2.Asset(file, filename, filetype, metadata)


def serve(port=5000, max_workers=4):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    opac_pb2.add_AssetServiceServicer_to_server(Asset(), server)
    server.add_insecure_port('[::]:{0}'.format(port))
    server.start()

    print('Started GRPC server on locahost, port: {0}, accept connections!'.format(port))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
