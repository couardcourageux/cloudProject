import os, sys
LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "grpc"))

from kvStoreClient import KvStoreClient


from agentNode import Node, AdressHolder, Agent
from key import HashKey

from connectionDealer import ConnectionNotFoundException, decoTryConnection

class LocalNodeLib:
    
    @classmethod
    async def check_predecessor(self, node:'Node') -> bool:
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator, n_addr=-1)
        async def func(distantAgentHost:str):
            try:
                await KvStoreClient.ping(distantAgentHost)
                return True
            except ConnectionNotFoundException as err:
                return False
            
        return await func()
    
    @classmethod
    async def make_check_predecessor(self, node:'Node') -> bool:
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator, n_addr=-1)
        async def func(distantAgentHost:str):
            try:
                await KvStoreClient.checkPredecessor(distantAgentHost)
                return True
            except ConnectionNotFoundException as err:
                return False
        return await func()
    
    
    @classmethod
    async def find_successor(self, hashKey:str, node:'Node', withNeighbors:bool=False):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator, n_addr=-1)
        async def func(hashKey:str, withNeighbors:bool, distantAgentHost:str):
            try:
                truc =  await KvStoreClient.findSuccessor(distantAgentHost, hashKey, withNeighbors=withNeighbors if withNeighbors else False)
                return truc
            except  ConnectionNotFoundException as err:
                raise err
        return await func(hashKey, withNeighbors)
               
               
               
                
    @classmethod
    async def updatePredecessor(self, callingNodeDesc:dict, node:'Node'):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator)
        async def func(callingNodeDesc:dict, distantAgentHost:str):
            try:
                return await KvStoreClient.updatePredecessor(distantAgentHost, callingNodeDesc)
            except  ConnectionNotFoundException as err:
                raise err
        return await func(callingNodeDesc)
    
    @classmethod
    async def updateSuccessor(self, callingNodeDesc:dict, node:'Node'):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator)
        async def func(callingNodeDesc:dict, distantAgentHost:str):
            try:
                return await KvStoreClient.updateSuccessor(distantAgentHost, callingNodeDesc)
            except  ConnectionNotFoundException as err:
                raise err
        return await func(callingNodeDesc)
    
    @classmethod
    async def updateFingerTable(self, callingNodeDescriptorFull, i, node):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator)
        async def func(callingNodeDescriptorFull:dict, i:int, distantAgentHost:str):
            try:
                return await KvStoreClient.updateFingerTable(distantAgentHost, callingNodeDescriptorFull, i)
            except  ConnectionNotFoundException as err:
                raise err
        return await func(callingNodeDescriptorFull, i)
    
    @classmethod
    async def getUpdatedDescriptor(self, node):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator)
        async def func(distantAgentHost:str):
            try:
                return await KvStoreClient.getUpdatedDhtDescriptor(distantAgentHost)
            except  ConnectionNotFoundException as err:
                raise err
        return await func()
    
    
    @classmethod
    async def notify_new_predecessor(self, newPredDesc:dict, node):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator)
        async def func(distantAgentHost:str):
            try:
                return await KvStoreClient.notifyNewPred(distantAgentHost, newPredDesc)
            except  ConnectionNotFoundException as err:
                raise err
        return await func(newPredDesc)
    
    
    