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




class Holder:
    dhtNode = None
    
    @classmethod
    def setDhtNode(self, node: DhtNode) -> None:
        self.dhtNode = node
    
    @classmethod
    def getDhtNode(self) -> DhtNode:
        return self.dhtNode


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
    # Holder.setDhtNode(dhtNode)
    DhtNode.register(dhtNode)
    
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
        res = await dhtNode._find_successor_rec(localHashKey, True)
        print(res)
    
    asyncio.run(runTest())
    
    
    # print(dhtNode.toDict())
    
    # asyncio.run(serve(5005))
    