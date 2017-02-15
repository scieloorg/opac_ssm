import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2


class AssetServiceStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.get_asset = channel.unary_unary(
        '/AssetService/get_asset',
        request_serializer=opac__pb2.TaskId.SerializeToString,
        response_deserializer=opac__pb2.Asset.FromString,
        )
    self.add_asset = channel.unary_unary(
        '/AssetService/add_asset',
        request_serializer=opac__pb2.Asset.SerializeToString,
        response_deserializer=opac__pb2.TaskId.FromString,
        )
    self.get_asset_info = channel.unary_unary(
        '/AssetService/get_asset_info',
        request_serializer=opac__pb2.TaskId.SerializeToString,
        response_deserializer=opac__pb2.AssetInfo.FromString,
        )
    self.get_task_state = channel.unary_unary(
        '/AssetService/get_task_state',
        request_serializer=opac__pb2.TaskId.SerializeToString,
        response_deserializer=opac__pb2.TaskState.FromString,
        )


class AssetServiceServicer(object):

  def get_asset(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def add_asset(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def get_asset_info(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def get_task_state(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AssetServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'get_asset': grpc.unary_unary_rpc_method_handler(
          servicer.get_asset,
          request_deserializer=opac__pb2.TaskId.FromString,
          response_serializer=opac__pb2.Asset.SerializeToString,
      ),
      'add_asset': grpc.unary_unary_rpc_method_handler(
          servicer.add_asset,
          request_deserializer=opac__pb2.Asset.FromString,
          response_serializer=opac__pb2.TaskId.SerializeToString,
      ),
      'get_asset_info': grpc.unary_unary_rpc_method_handler(
          servicer.get_asset_info,
          request_deserializer=opac__pb2.TaskId.FromString,
          response_serializer=opac__pb2.AssetInfo.SerializeToString,
      ),
      'get_task_state': grpc.unary_unary_rpc_method_handler(
          servicer.get_task_state,
          request_deserializer=opac__pb2.TaskId.FromString,
          response_serializer=opac__pb2.TaskState.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'AssetService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
