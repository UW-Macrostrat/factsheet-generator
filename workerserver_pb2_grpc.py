# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import workerserver_pb2 as workerserver__pb2


class WorkerServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StoreFile = channel.unary_unary(
                '/WorkerServer/StoreFile',
                request_serializer=workerserver__pb2.FileDataRequest.SerializeToString,
                response_deserializer=workerserver__pb2.ErrorResponse.FromString,
                )
        self.SetStratNames = channel.unary_unary(
                '/WorkerServer/SetStratNames',
                request_serializer=workerserver__pb2.StratNameRequest.SerializeToString,
                response_deserializer=workerserver__pb2.ErrorResponse.FromString,
                )
        self.SetQueries = channel.unary_unary(
                '/WorkerServer/SetQueries',
                request_serializer=workerserver__pb2.QueryRequest.SerializeToString,
                response_deserializer=workerserver__pb2.ErrorResponse.FromString,
                )
        self.GenerateFacts = channel.unary_unary(
                '/WorkerServer/GenerateFacts',
                request_serializer=workerserver__pb2.FactRequest.SerializeToString,
                response_deserializer=workerserver__pb2.ErrorResponse.FromString,
                )


class WorkerServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StoreFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetStratNames(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetQueries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GenerateFacts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkerServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StoreFile': grpc.unary_unary_rpc_method_handler(
                    servicer.StoreFile,
                    request_deserializer=workerserver__pb2.FileDataRequest.FromString,
                    response_serializer=workerserver__pb2.ErrorResponse.SerializeToString,
            ),
            'SetStratNames': grpc.unary_unary_rpc_method_handler(
                    servicer.SetStratNames,
                    request_deserializer=workerserver__pb2.StratNameRequest.FromString,
                    response_serializer=workerserver__pb2.ErrorResponse.SerializeToString,
            ),
            'SetQueries': grpc.unary_unary_rpc_method_handler(
                    servicer.SetQueries,
                    request_deserializer=workerserver__pb2.QueryRequest.FromString,
                    response_serializer=workerserver__pb2.ErrorResponse.SerializeToString,
            ),
            'GenerateFacts': grpc.unary_unary_rpc_method_handler(
                    servicer.GenerateFacts,
                    request_deserializer=workerserver__pb2.FactRequest.FromString,
                    response_serializer=workerserver__pb2.ErrorResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'WorkerServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WorkerServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StoreFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WorkerServer/StoreFile',
            workerserver__pb2.FileDataRequest.SerializeToString,
            workerserver__pb2.ErrorResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetStratNames(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WorkerServer/SetStratNames',
            workerserver__pb2.StratNameRequest.SerializeToString,
            workerserver__pb2.ErrorResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetQueries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WorkerServer/SetQueries',
            workerserver__pb2.QueryRequest.SerializeToString,
            workerserver__pb2.ErrorResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GenerateFacts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WorkerServer/GenerateFacts',
            workerserver__pb2.FactRequest.SerializeToString,
            workerserver__pb2.ErrorResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)