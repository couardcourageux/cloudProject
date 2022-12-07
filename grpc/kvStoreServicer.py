import protocol_pb2
import protocol_pb2_grpc
import asyncio

class KvStoreServicer(protocol_pb2_grpc.KvStoreServicer):
    async def ping(self, request, context):
        return protocol_pb2.VoidMsg()
        
    
    async def obtainId(self, request, context):
        print("waiting now obtainId")
        resp = protocol_pb2.PayloadMsg()
        #things to do
        return resp
    
    async def findNode(self, request, context):
        print("waiting now findNode")
        resp = protocol_pb2.PayloadMsg()
        #things to do
        return resp
    
    
