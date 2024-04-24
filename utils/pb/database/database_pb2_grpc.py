# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import database_pb2 as database__pb2


class DatabaseServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Read = channel.unary_unary(
                '/database.DatabaseService/Read',
                request_serializer=database__pb2.ReadRequest.SerializeToString,
                response_deserializer=database__pb2.ReadResponse.FromString,
                )
        self.PrepareWrite = channel.unary_unary(
                '/database.DatabaseService/PrepareWrite',
                request_serializer=database__pb2.PrepareWriteRequest.SerializeToString,
                response_deserializer=database__pb2.PrepareResponse.FromString,
                )
        self.CommitWrite = channel.unary_unary(
                '/database.DatabaseService/CommitWrite',
                request_serializer=database__pb2.CommitRequest.SerializeToString,
                response_deserializer=database__pb2.CommitResponse.FromString,
                )
        self.PrepareDecrementStock = channel.unary_unary(
                '/database.DatabaseService/PrepareDecrementStock',
                request_serializer=database__pb2.PrepareDecrementStockRequest.SerializeToString,
                response_deserializer=database__pb2.PrepareResponse.FromString,
                )
        self.CommitDecrementStock = channel.unary_unary(
                '/database.DatabaseService/CommitDecrementStock',
                request_serializer=database__pb2.CommitRequest.SerializeToString,
                response_deserializer=database__pb2.CommitResponse.FromString,
                )


class DatabaseServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PrepareWrite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CommitWrite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PrepareDecrementStock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CommitDecrementStock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DatabaseServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Read': grpc.unary_unary_rpc_method_handler(
                    servicer.Read,
                    request_deserializer=database__pb2.ReadRequest.FromString,
                    response_serializer=database__pb2.ReadResponse.SerializeToString,
            ),
            'PrepareWrite': grpc.unary_unary_rpc_method_handler(
                    servicer.PrepareWrite,
                    request_deserializer=database__pb2.PrepareWriteRequest.FromString,
                    response_serializer=database__pb2.PrepareResponse.SerializeToString,
            ),
            'CommitWrite': grpc.unary_unary_rpc_method_handler(
                    servicer.CommitWrite,
                    request_deserializer=database__pb2.CommitRequest.FromString,
                    response_serializer=database__pb2.CommitResponse.SerializeToString,
            ),
            'PrepareDecrementStock': grpc.unary_unary_rpc_method_handler(
                    servicer.PrepareDecrementStock,
                    request_deserializer=database__pb2.PrepareDecrementStockRequest.FromString,
                    response_serializer=database__pb2.PrepareResponse.SerializeToString,
            ),
            'CommitDecrementStock': grpc.unary_unary_rpc_method_handler(
                    servicer.CommitDecrementStock,
                    request_deserializer=database__pb2.CommitRequest.FromString,
                    response_serializer=database__pb2.CommitResponse.SerializeToString,
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
            database__pb2.ReadRequest.SerializeToString,
            database__pb2.ReadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PrepareWrite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/database.DatabaseService/PrepareWrite',
            database__pb2.PrepareWriteRequest.SerializeToString,
            database__pb2.PrepareResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CommitWrite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/database.DatabaseService/CommitWrite',
            database__pb2.CommitRequest.SerializeToString,
            database__pb2.CommitResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PrepareDecrementStock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/database.DatabaseService/PrepareDecrementStock',
            database__pb2.PrepareDecrementStockRequest.SerializeToString,
            database__pb2.PrepareResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CommitDecrementStock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/database.DatabaseService/CommitDecrementStock',
            database__pb2.CommitRequest.SerializeToString,
            database__pb2.CommitResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
