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
    
    dhtNode = DhtNode(
        local=True,
        id=HashKey.getRandom()
    )
    localHashKey = dhtNode.id
    dhtNode._predecessor = localHashKey
    dhtNode._Successor._successor = localHashKey
    Holder.setDhtNode(dhtNode)
    
    localNode = Node(localHashKey.hashValue)
    Node.register(localNode)
    
    localAgent = Agent(
        HashKey.getRandom().value,
        "localhost", 
        "5005", 
        localNode.id
    )
    Agent.register(localAgent)
    localNode.addAgent(localAgent.id)
    
    
    
    
    asyncio.run(serve(5000))
    