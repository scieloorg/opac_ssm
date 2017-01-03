import grpc

import opac_ssm_pb2


def run():
    channel = grpc.insecure_channel('localhost:5000')

    stub = opac_ssm_pb2.AssetServiceStub(channel)

    asset = stub.add_asset(opac_ssm_pb2.Asset(file=open('opac_ssm.proto', 'rb').read(), type="img", metadata="CC-BY"))

    print(asset.file, asset.type, asset.metadata)

if __name__ == '__main__':
    run()
