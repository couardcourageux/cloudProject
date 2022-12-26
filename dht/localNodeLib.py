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
            await KvStoreClient.ping(distantAgentHost)
              
        try:
            await func()
            return True
        except ConnectionNotFoundException as err:
            return False
    
    @classmethod
    async def make_check_predecessor(self, node:'Node') -> bool:
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator, n_addr=-1)
        async def func(distantAgentHost:str):
            await KvStoreClient.checkPredecessor(distantAgentHost)
  
        try:
            await func()
            return True
        except ConnectionNotFoundException as err:
            return False
    
    
    @classmethod
    async def find_successor(self, hashKey:str, node:'Node', withNeighbors:bool=False):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator, n_addr=-1)
        async def func(hashKey:str, withNeighbors:bool, distantAgentHost:str):
            return await KvStoreClient.findSuccessor(distantAgentHost, hashKey, withNeighbors=withNeighbors if withNeighbors else False) 
        try:
            return await func(hashKey, withNeighbors)
        except  ConnectionNotFoundException as err:
            print(f"{err=}, {type(err)=}")
               
               
               
                
    @classmethod
    async def updatePredecessor(self, callingNodeDesc:dict, node:'Node'):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator)
        async def func(callingNodeDesc:dict, distantAgentHost:str):
            return await KvStoreClient.updatePredecessor(distantAgentHost, callingNodeDesc)

        try:
            return await func(callingNodeDesc)
        except  ConnectionNotFoundException as err:
            print(f"{err=}, {type(err)=}")
    
    @classmethod
    async def updateSuccessor(self, callingNodeDesc:dict, node:'Node'):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator)
        async def func(callingNodeDesc:dict, distantAgentHost:str):
            return await KvStoreClient.updateSuccessor(distantAgentHost, callingNodeDesc)
            
        try:
            return await func(callingNodeDesc)
        except  ConnectionNotFoundException as err:
            print(f"{err=}, {type(err)=}")
            
    @classmethod
    async def updateFingerTable(self, callingNodeDescriptorFull, i, node):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator)
        async def func(callingNodeDescriptorFull:dict, i:int, distantAgentHost:str):
            return await KvStoreClient.updateFingerTable(distantAgentHost, callingNodeDescriptorFull, i)
            
            
        try:
            return await func(callingNodeDescriptorFull, i)
        except  ConnectionNotFoundException as err:
            print(f"{err=}, {type(err)=}")
        
    @classmethod
    async def getUpdatedDescriptor(self, node):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator)
        async def func(distantAgentHost:str):
            return await KvStoreClient.getUpdatedDhtDescriptor(distantAgentHost) 
        try:
            return await func()
        except  ConnectionNotFoundException as err:
            print(f"{err=}, {type(err)=}")
    
    
    @classmethod
    async def notify_new_predecessor(self, newPredDesc:dict, node):
        iterator = node.getAgentsIterator()
        
        @decoTryConnection(iterator)
        async def func(distantAgentHost:str):
            return await KvStoreClient.notifyNewPred(distantAgentHost, newPredDesc)
        try:
            return await func(newPredDesc)
        except  ConnectionNotFoundException as err:
            print(f"{err=}, {type(err)=}")
    
    
    