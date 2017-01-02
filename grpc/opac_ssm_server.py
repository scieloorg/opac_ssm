
from concurrent import futures
import time

import grpc

import opac_ssm_pb2

class Asset(opac_ssm_pb2.AssetServiceServicer):

  def add_asset(self, request, context):
    """
    Return a Asset object
    """
    return opac_ssm_pb2.Asset(file=request.file, origin=request.origin,
                            license=request.license,
                            visibility=request.visibility,
                            metadata=request.metadata,
                            description=request.description)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  opac_ssm_pb2.add_AssetServiceServicer_to_server(Asset(), server)
  server.add_insecure_port('[::]:5000')
  server.start()

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()