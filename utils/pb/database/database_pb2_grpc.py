# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from utils.pb.database import database_pb2 as utils_dot_pb_dot_database_dot_database__pb2


class DatabaseServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Read = channel.unary_unary(
                '/database.DatabaseService/Read',
                request_serializer=utils_dot_pb_dot_database_dot_database__pb2.ReadRequest.SerializeToString,
                response_deserializer=utils_dot_pb_dot_database_dot_database__pb2.ReadResponse.FromString,
                )
        self.Write = channel.unary_unary(
                '/database.DatabaseService/Write',
                request_serializer=utils_dot_pb_dot_database_dot_database__pb2.WriteRequest.SerializeToString,
                response_deserializer=utils_dot_pb_dot_database_dot_database__pb2.WriteResponse.FromString,
                )
        self.DecrementStock = channel.unary_unary(
                '/database.DatabaseService/DecrementStock',
                request_serializer=utils_dot_pb_dot_database_dot_database__pb2.DecrementStockRequest.SerializeToString,
                response_deserializer=utils_dot_pb_dot_database_dot_database__pb2.DecrementStockResponse.FromString,
                )


class DatabaseServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Write(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DecrementStock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DatabaseServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Read': grpc.unary_unary_rpc_method_handler(
                    servicer.Read,
                    request_deserializer=utils_dot_pb_dot_database_dot_database__pb2.ReadRequest.FromString,
                    response_serializer=utils_dot_pb_dot_database_dot_database__pb2.ReadResponse.SerializeToString,
            ),
            'Write': grpc.unary_unary_rpc_method_handler(
                    servicer.Write,
                    request_deserializer=utils_dot_pb_dot_database_dot_database__pb2.WriteRequest.FromString,
                    response_serializer=utils_dot_pb_dot_database_dot_database__pb2.WriteResponse.SerializeToString,
            ),
            'DecrementStock': grpc.unary_unary_rpc_method_handler(
                    servicer.DecrementStock,
                    request_deserializer=utils_dot_pb_dot_database_dot_database__pb2.DecrementStockRequest.FromString,
                    response_serializer=utils_dot_pb_dot_database_dot_database__pb2.DecrementStockResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'database.DatabaseService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DatabaseService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Read(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/database.DatabaseService/Read',
            utils_dot_pb_dot_database_dot_database__pb2.ReadRequest.SerializeToString,
            utils_dot_pb_dot_database_dot_database__pb2.ReadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Write(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/database.DatabaseService/Write',
            utils_dot_pb_dot_database_dot_database__pb2.WriteRequest.SerializeToString,
            utils_dot_pb_dot_database_dot_database__pb2.WriteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DecrementStock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/database.DatabaseService/DecrementStock',
            utils_dot_pb_dot_database_dot_database__pb2.DecrementStockRequest.SerializeToString,
            utils_dot_pb_dot_database_dot_database__pb2.DecrementStockResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
