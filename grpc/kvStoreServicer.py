import os, sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "dht"))

import protocol_pb2
import protocol_pb2_grpc
import asyncio
import json
from signalHandler import SignalHandler


from dhtNode import DhtNode

class KvStoreServicer(protocol_pb2_grpc.KvStoreServicer):
    async def ping(self, request, context):
        print("pinged")
        return protocol_pb2.VoidMsg()
        
    async def obtainId(self, request, context):
        print("waiting now obtainId")
        localDhtNode = DhtNode.getLocal()
        resp = protocol_pb2.PayloadMsg()
        #things to do
        return resp
    
    async def findSuccessor(self, request, context):
        localDhtNode = DhtNode.getLocal()
        reqData = json.loads(request.jsonData)
        print("from distance")
        repData = await localDhtNode.find_successor(reqData["hashValue"], reqData["withNeighbors"])
        resp = protocol_pb2.PayloadMsg()
        resp.respStatus = 0
        resp.jsonData = json.dumps(repData)
        return resp
    
    async def checkPredecessor(self, request, context):
        localDhtNode = DhtNode.getLocal()
        await localDhtNode.checkPredecessor()
        return protocol_pb2.VoidMsg()
    
    async def getUpdatedDhtDescriptor(self, request, context):
        localDhtNode = DhtNode.getLocal()
        repData = await localDhtNode.find_successor(localDhtNode.id)     
        
        resp = protocol_pb2.PayloadMsg()
        resp.respStatus = 0
        resp.jsonData = json.dumps(repData)
        return resp
        
    async def updateFingerTable(self, request, context):
        localDhtNode = DhtNode.getLocal()
        reqData = json.loads(request.jsonData)
        await localDhtNode._update_finger_table(
            reqData["callingNodeDescriptorFull"], 
            reqData["i"]
        )
        return protocol_pb2.VoidMsg()
    
    async def updateSuccessor(self, request, context):
        localDhtNode = DhtNode.getLocal()
        reqData = json.loads(request.jsonData)
        await localDhtNode.update_successor(
            reqData["callingNodeDescriptorFull"]
        )
        return protocol_pb2.VoidMsg()
    
    
    async def updatePredecessor(self, request, context):
        localDhtNode = DhtNode.getLocal()
        reqData = json.loads(request.jsonData)
        await localDhtNode.update_predecessor(
            reqData["callingNodeDescriptorFull"]
        )
        return protocol_pb2.VoidMsg()
    
    async def notifyNewPred(self, request, context):
        reqData = json.loads(request.jsonData)
        localDhtNode = DhtNode.getLocal()
        await localDhtNode.notify_new_pred(reqData["newPredDescFull"])
        return protocol_pb2.VoidMsg()
    
    async def plzDie(self, request, context):
        await SignalHandler.stopGrpcServer()
        return protocol_pb2.VoidMsg()
        
        
        
        
    
    

    
    
