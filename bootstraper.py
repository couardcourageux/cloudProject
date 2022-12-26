import os
import sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "grpc"))
sys.path.append(os.path.join(LOCAL_DIRECTORY, "dht"))
sys.path.append(os.path.join(LOCAL_DIRECTORY, "nodesAgent"))


from server import serve
import asyncio


from dhtNode import DhtNode
from key import HashKey
from agentNode import Agent, Node
from kvStoreClient import KvStoreClient



if __name__ == "__main__":
    
    
    localHashKey = HashKey.getRandom()
    dhtNode = DhtNode(
        local=True,
        id=localHashKey,
        _predecessor=localHashKey,
        _successor=localHashKey,
        _finger=[None for i in range(256)]
    )
    
    dhtNode._finger[0] = localHashKey
    DhtNode.register(dhtNode)
    dhtNode.setLocal()
    
    localNode = Node(localHashKey.hashValue)
    Node.register(localNode)
    
    localAgent = Agent(
        HashKey.getRandom().value,
        "localhost", 
        "5005", 
        0
    )
    Agent.register(localAgent)
    localNode.addAgent(localAgent.id)
    
    async def runTest():
        await asyncio.sleep(9)
        print(await dhtNode._is_alive())
        print(await DhtNode.get(dhtNode._predecessor)._is_alive())
        print(await dhtNode.check_predecessor())
        await KvStoreClient.plzDie("localhost:5006")
        # await KvStoreClient.plzDie("localhost:5007")
        await asyncio.sleep(4)
        print(await dhtNode.check_predecessor())
        print(await DhtNode.get(dhtNode._predecessor)._is_alive())
        print(await dhtNode._is_alive())
        
    async def yehyehTest():
        await asyncio.gather(runTest(), serve(5005))
        
        
    asyncio.run(serve(5005))
    # asyncio.run(yehyehTest())
    