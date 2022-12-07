from grpc import aio
import asyncio
import json

import protocol_pb2
import protocol_pb2_grpc


class KvStoreClient():
    
    @classmethod
    async def join_network(self, distantAgentHost:str) -> tuple:
        async with aio.insecure_channel(distantAgentHost) as ch:
            stub = protocol_pb2_grpc.KvStoreStub(ch)
            req = protocol_pb2.VoidMsg()
            response = await stub.obtainId(req, timeout=40)
            #smth to do now
            
            
    @classmethod
    async def searchNode(self, distantAgentHost:str, RingId:str) -> dict:
        async with aio.insecure_channel(distantAgentHost) as ch:
            stub = protocol_pb2_grpc.KvStoreStub(ch)
            req = protocol_pb2.PayloadMsg()
            # req.respStatus = 0
            # req.jsonData = json.dumps({
            #     'RingId':RingId
            # })
            
            response = await stub.findNode(req, timeout=15)
            # if response.respStatus:
            #     return None
            #     #we need to raise an exception instead of return None
            # return json.loads(response.jsonData)
            return {}
            #smth to do now