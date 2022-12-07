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
            
        
        
        
        
        # return True