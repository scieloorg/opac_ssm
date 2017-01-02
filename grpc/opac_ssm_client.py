import grpc

import opac_ssm_pb2

def run():
    channel = grpc.insecure_channel('localhost:5000')

    stub = opac_ssm_pb2.AssetServiceStub(channel)

    asset = stub.add_asset(opac_ssm_pb2.Asset(file=open('PATH').read(), origin="from grpc", license="CC-BY"))

    print asset.file, asset.origin, asset.license

if __name__ == '__main__':
    run()
