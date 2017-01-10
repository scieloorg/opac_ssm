#!/usr/bin/env python

import os
import grpc

import opac_pb2


def run():
    channel = grpc.insecure_channel('localhost:5000')

    stub = opac_pb2.AssetServiceStub(channel)

    file = open('sample.txt', 'rb')

    filename = os.path.basename(getattr(file, 'name', None))

    meta = "{'foo': 'bar', 'pickles': 'blaus'}" # String

    asset = stub.add_asset(opac_pb2.Asset(file=file.read(), filename=filename,
                                          type="txt", metadata=meta))

    print(asset)

if __name__ == '__main__':
    run()
