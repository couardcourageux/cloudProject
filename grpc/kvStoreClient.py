from grpc import aio
import asyncio
import json

import protocol_pb2
import protocol_pb2_grpc


class KvStoreClient():
    
    @classmethod
    async def ping(self, distantAgentHost:str) -> None:
        async with aio.insecure_channel(distantAgentHost) as ch:
            stub = protocol_pb2_grpc.KvStoreStub(ch)
            req = protocol_pb2.VoidMsg()
            await stub.obtainId(req, timeout=5)
            return 
        
    
    @classmethod
    async def join_network(self, distantAgentHost:str) -> tuple:
        async with aio.insecure_channel(distantAgentHost) as ch:
            stub = protocol_pb2_grpc.KvStoreStub(ch)
            req = protocol_pb2.VoidMsg()
            response = await stub.obtainId(req, timeout=40)
            #smth to do now
            
            
    @classmethod
    async def findSuccessor(self, distantAgentHost:str, hashValue:str, withNeighbors:bool=False) -> dict:
        async with aio.insecure_channel(distantAgentHost) as ch:
            stub = protocol_pb2_grpc.KvStoreStub(ch)
            req = protocol_pb2.PayloadMsg()
            req.respStatus = 0
            req.jsonData = json.dumps({
                "hashValue":hashValue,
                "withNeighbors": withNeighbors
            })
            
            response = await stub.findSuccessor(req, timeout=15)
        if response.respStatus:
            return None
        #     #we need to raise an exception instead of return None
        return json.loads(response.jsonData)
        
    @classmethod
    async def checkPredecessor(self, distantAgentHost:str):
        async with aio.insecure_channel(distantAgentHost) as ch:
            stub = protocol_pb2_grpc.KvStoreStub(ch)
            await stub.checkPredecessor(protocol_pb2.VoidMsg())
        return
    
    @classmethod
    async def getUpdatedDhtDescriptor(self, distantAgentHost:str):
        async with aio.insecure_channel(distantAgentHost) as ch:
            stub = protocol_pb2_grpc.KvStoreStub(ch)
            resp = await stub.getUpdatedDhtDescriptor(protocol_pb2.VoidMsg())

        if resp.respStatus:
            return None
        #     #we need to raise an exception instead of return None
        return json.loads(resp.jsonData)
    
    @classmethod
    async def updateFingerTable(self, distantAgentHost:str, callingNodeDescriptorFull:dict, i:int):
        req = protocol_pb2.PayloadMsg()
        req.respStatus = 0
        req.jsonData = json.dumps({
            "callingNodeDescriptorFull":callingNodeDescriptorFull,
            "i":i
        })
        
        async with aio.insecure_channel(distantAgentHost) as ch:
            stub = protocol_pb2_grpc.KvStoreStub(ch)
            await stub.updateFingerTable(req)
            
        return

    @classmethod
    async def updateSuccessor(self, distantAgentHost:str, callingNodeDescriptorFull:dict):
        req = protocol_pb2.PayloadMsg()
        req.respStatus = 0
        req.jsonData = json.dumps({
            "callingNodeDescriptorFull":callingNodeDescriptorFull
        })
        
        async with aio.insecure_channel(distantAgentHost) as ch:
            stub = protocol_pb2_grpc.KvStoreStub(ch)
            await stub.updateSuccessor(req)
            
    @classmethod
    async def updatePredecessor(self, distantAgentHost:str, callingNodeDescriptorFull:dict):
        req = protocol_pb2.PayloadMsg()
        req.respStatus = 0
        req.jsonData = json.dumps({
            "callingNodeDescriptorFull":callingNodeDescriptorFull
        })
        
        async with aio.insecure_channel(distantAgentHost) as ch:
            stub = protocol_pb2_grpc.KvStoreStub(ch)
            await stub.updatePredecessor(req)

            