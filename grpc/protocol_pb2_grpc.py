# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protocol_pb2 as protocol__pb2


class KvStoreStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ping = channel.unary_unary(
                '/KVStore.KvStore/ping',
                request_serializer=protocol__pb2.VoidMsg.SerializeToString,
                response_deserializer=protocol__pb2.VoidMsg.FromString,
                )
        self.obtainId = channel.unary_unary(
                '/KVStore.KvStore/obtainId',
                request_serializer=protocol__pb2.VoidMsg.SerializeToString,
                response_deserializer=protocol__pb2.PayloadMsg.FromString,
                )
        self.findSuccessor = channel.unary_unary(
                '/KVStore.KvStore/findSuccessor',
                request_serializer=protocol__pb2.PayloadMsg.SerializeToString,
                response_deserializer=protocol__pb2.PayloadMsg.FromString,
                )
        self.checkPredecessor = channel.unary_unary(
                '/KVStore.KvStore/checkPredecessor',
                request_serializer=protocol__pb2.VoidMsg.SerializeToString,
                response_deserializer=protocol__pb2.VoidMsg.FromString,
                )
        self.getUpdatedDhtDescriptor = channel.unary_unary(
                '/KVStore.KvStore/getUpdatedDhtDescriptor',
                request_serializer=protocol__pb2.VoidMsg.SerializeToString,
                response_deserializer=protocol__pb2.PayloadMsg.FromString,
                )
        self.updateFingerTable = channel.unary_unary(
                '/KVStore.KvStore/updateFingerTable',
                request_serializer=protocol__pb2.PayloadMsg.SerializeToString,
                response_deserializer=protocol__pb2.VoidMsg.FromString,
                )
        self.updateSuccessor = channel.unary_unary(
                '/KVStore.KvStore/updateSuccessor',
                request_serializer=protocol__pb2.PayloadMsg.SerializeToString,
                response_deserializer=protocol__pb2.VoidMsg.FromString,
                )
        self.updatePredecessor = channel.unary_unary(
                '/KVStore.KvStore/updatePredecessor',
                request_serializer=protocol__pb2.PayloadMsg.SerializeToString,
                response_deserializer=protocol__pb2.VoidMsg.FromString,
                )


class KvStoreServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def obtainId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def findSuccessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkPredecessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getUpdatedDhtDescriptor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def updateFingerTable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def updateSuccessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def updatePredecessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KvStoreServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ping': grpc.unary_unary_rpc_method_handler(
                    servicer.ping,
                    request_deserializer=protocol__pb2.VoidMsg.FromString,
                    response_serializer=protocol__pb2.VoidMsg.SerializeToString,
            ),
            'obtainId': grpc.unary_unary_rpc_method_handler(
                    servicer.obtainId,
                    request_deserializer=protocol__pb2.VoidMsg.FromString,
                    response_serializer=protocol__pb2.PayloadMsg.SerializeToString,
            ),
            'findSuccessor': grpc.unary_unary_rpc_method_handler(
                    servicer.findSuccessor,
                    request_deserializer=protocol__pb2.PayloadMsg.FromString,
                    response_serializer=protocol__pb2.PayloadMsg.SerializeToString,
            ),
            'checkPredecessor': grpc.unary_unary_rpc_method_handler(
                    servicer.checkPredecessor,
                    request_deserializer=protocol__pb2.VoidMsg.FromString,
                    response_serializer=protocol__pb2.VoidMsg.SerializeToString,
            ),
            'getUpdatedDhtDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.getUpdatedDhtDescriptor,
                    request_deserializer=protocol__pb2.VoidMsg.FromString,
                    response_serializer=protocol__pb2.PayloadMsg.SerializeToString,
            ),
            'updateFingerTable': grpc.unary_unary_rpc_method_handler(
                    servicer.updateFingerTable,
                    request_deserializer=protocol__pb2.PayloadMsg.FromString,
                    response_serializer=protocol__pb2.VoidMsg.SerializeToString,
            ),
            'updateSuccessor': grpc.unary_unary_rpc_method_handler(
                    servicer.updateSuccessor,
                    request_deserializer=protocol__pb2.PayloadMsg.FromString,
                    response_serializer=protocol__pb2.VoidMsg.SerializeToString,
            ),
            'updatePredecessor': grpc.unary_unary_rpc_method_handler(
                    servicer.updatePredecessor,
                    request_deserializer=protocol__pb2.PayloadMsg.FromString,
                    response_serializer=protocol__pb2.VoidMsg.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'KVStore.KvStore', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KvStore(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KVStore.KvStore/ping',
            protocol__pb2.VoidMsg.SerializeToString,
            protocol__pb2.VoidMsg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def obtainId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KVStore.KvStore/obtainId',
            protocol__pb2.VoidMsg.SerializeToString,
            protocol__pb2.PayloadMsg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def findSuccessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KVStore.KvStore/findSuccessor',
            protocol__pb2.PayloadMsg.SerializeToString,
            protocol__pb2.PayloadMsg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def checkPredecessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KVStore.KvStore/checkPredecessor',
            protocol__pb2.VoidMsg.SerializeToString,
            protocol__pb2.VoidMsg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getUpdatedDhtDescriptor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KVStore.KvStore/getUpdatedDhtDescriptor',
            protocol__pb2.VoidMsg.SerializeToString,
            protocol__pb2.PayloadMsg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def updateFingerTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KVStore.KvStore/updateFingerTable',
            protocol__pb2.PayloadMsg.SerializeToString,
            protocol__pb2.VoidMsg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def updateSuccessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KVStore.KvStore/updateSuccessor',
            protocol__pb2.PayloadMsg.SerializeToString,
            protocol__pb2.VoidMsg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def updatePredecessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KVStore.KvStore/updatePredecessor',
            protocol__pb2.PayloadMsg.SerializeToString,
            protocol__pb2.VoidMsg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
