import protocol_pb2
import protocol_pb2_grpc
import asyncio

class KvStoreServicer(protocol_pb2_grpc.KvStoreServicer):
    async def obtainId(self, request, context):
        print("waiting now obtainId")
        await asyncio.sleep(30)
        resp = protocol_pb2.PayloadMsg()
        
        #things to do
        return resp
    
    async def findNode(self, request, context):
        print("waiting now findNode")
        await asyncio.sleep(3)
        resp = protocol_pb2.PayloadMsg()
        
        #things to do
        print("jai fini batard")
        return resp