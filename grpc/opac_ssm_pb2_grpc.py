import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import opac_ssm_pb2 as opac__ssm__pb2
import opac_ssm_pb2 as opac__ssm__pb2


class AssetServiceStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.add_asset = channel.unary_unary(
        '/AssetService/add_asset',
        request_serializer=opac__ssm__pb2.Asset.SerializeToString,
        response_deserializer=opac__ssm__pb2.Asset.FromString,
        )


class AssetServiceServicer(object):

  def add_asset(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AssetServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'add_asset': grpc.unary_unary_rpc_method_handler(
          servicer.add_asset,
          request_deserializer=opac__ssm__pb2.Asset.FromString,
          response_serializer=opac__ssm__pb2.Asset.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'AssetService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
