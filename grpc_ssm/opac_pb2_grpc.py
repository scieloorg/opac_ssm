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
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
import opac_pb2 as opac__pb2
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
    self.update_asset = channel.unary_unary(
        '/AssetService/update_asset',
        request_serializer=opac__pb2.Asset.SerializeToString,
        response_deserializer=opac__pb2.TaskId.FromString,
        )
    self.remove_asset = channel.unary_unary(
        '/AssetService/remove_asset',
        request_serializer=opac__pb2.TaskId.SerializeToString,
        response_deserializer=opac__pb2.TaskId.FromString,
        )
    self.exists_asset = channel.unary_unary(
        '/AssetService/exists_asset',
        request_serializer=opac__pb2.TaskId.SerializeToString,
        response_deserializer=opac__pb2.AssetExists.FromString,
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
    self.get_bucket = channel.unary_unary(
        '/AssetService/get_bucket',
        request_serializer=opac__pb2.TaskId.SerializeToString,
        response_deserializer=opac__pb2.Bucket.FromString,
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

  def update_asset(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def remove_asset(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def exists_asset(self, request, context):
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

  def get_bucket(self, request, context):
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
      'update_asset': grpc.unary_unary_rpc_method_handler(
          servicer.update_asset,
          request_deserializer=opac__pb2.Asset.FromString,
          response_serializer=opac__pb2.TaskId.SerializeToString,
      ),
      'remove_asset': grpc.unary_unary_rpc_method_handler(
          servicer.remove_asset,
          request_deserializer=opac__pb2.TaskId.FromString,
          response_serializer=opac__pb2.TaskId.SerializeToString,
      ),
      'exists_asset': grpc.unary_unary_rpc_method_handler(
          servicer.exists_asset,
          request_deserializer=opac__pb2.TaskId.FromString,
          response_serializer=opac__pb2.AssetExists.SerializeToString,
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
      'get_bucket': grpc.unary_unary_rpc_method_handler(
          servicer.get_bucket,
          request_deserializer=opac__pb2.TaskId.FromString,
          response_serializer=opac__pb2.Bucket.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'AssetService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class BucketServiceStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.add_bucket = channel.unary_unary(
        '/BucketService/add_bucket',
        request_serializer=opac__pb2.BucketName.SerializeToString,
        response_deserializer=opac__pb2.TaskId.FromString,
        )
    self.update_bucket = channel.unary_unary(
        '/BucketService/update_bucket',
        request_serializer=opac__pb2.BucketName.SerializeToString,
        response_deserializer=opac__pb2.TaskId.FromString,
        )
    self.remove_bucket = channel.unary_unary(
        '/BucketService/remove_bucket',
        request_serializer=opac__pb2.BucketName.SerializeToString,
        response_deserializer=opac__pb2.TaskId.FromString,
        )
    self.exists_bucket = channel.unary_unary(
        '/BucketService/exists_bucket',
        request_serializer=opac__pb2.BucketName.SerializeToString,
        response_deserializer=opac__pb2.BucketExists.FromString,
        )
    self.get_assets = channel.unary_unary(
        '/BucketService/get_assets',
        request_serializer=opac__pb2.BucketName.SerializeToString,
        response_deserializer=opac__pb2.Assets.FromString,
        )


class BucketServiceServicer(object):

  def add_bucket(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def update_bucket(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def remove_bucket(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def exists_bucket(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def get_assets(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BucketServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'add_bucket': grpc.unary_unary_rpc_method_handler(
          servicer.add_bucket,
          request_deserializer=opac__pb2.BucketName.FromString,
          response_serializer=opac__pb2.TaskId.SerializeToString,
      ),
      'update_bucket': grpc.unary_unary_rpc_method_handler(
          servicer.update_bucket,
          request_deserializer=opac__pb2.BucketName.FromString,
          response_serializer=opac__pb2.TaskId.SerializeToString,
      ),
      'remove_bucket': grpc.unary_unary_rpc_method_handler(
          servicer.remove_bucket,
          request_deserializer=opac__pb2.BucketName.FromString,
          response_serializer=opac__pb2.TaskId.SerializeToString,
      ),
      'exists_bucket': grpc.unary_unary_rpc_method_handler(
          servicer.exists_bucket,
          request_deserializer=opac__pb2.BucketName.FromString,
          response_serializer=opac__pb2.BucketExists.SerializeToString,
      ),
      'get_assets': grpc.unary_unary_rpc_method_handler(
          servicer.get_assets,
          request_deserializer=opac__pb2.BucketName.FromString,
          response_serializer=opac__pb2.Assets.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'BucketService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
