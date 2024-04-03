# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from utils.pb.coordinator import coordinator_pb2 as utils_dot_pb_dot_coordinator_dot_coordinator__pb2


class CoordinatorServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Request = channel.unary_unary(
                '/coordinator.CoordinatorService/Request',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=utils_dot_pb_dot_coordinator_dot_coordinator__pb2.Message.FromString,
                )
        self.Release = channel.unary_unary(
                '/coordinator.CoordinatorService/Release',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=utils_dot_pb_dot_coordinator_dot_coordinator__pb2.Message.FromString,
                )


class CoordinatorServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Request(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Release(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CoordinatorServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Request': grpc.unary_unary_rpc_method_handler(
                    servicer.Request,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=utils_dot_pb_dot_coordinator_dot_coordinator__pb2.Message.SerializeToString,
            ),
            'Release': grpc.unary_unary_rpc_method_handler(
                    servicer.Release,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=utils_dot_pb_dot_coordinator_dot_coordinator__pb2.Message.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'coordinator.CoordinatorService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CoordinatorService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Request(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/coordinator.CoordinatorService/Request',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            utils_dot_pb_dot_coordinator_dot_coordinator__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Release(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/coordinator.CoordinatorService/Release',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            utils_dot_pb_dot_coordinator_dot_coordinator__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)