import os
import sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "grpc"))
sys.path.append(os.path.join(LOCAL_DIRECTORY, "dht"))
sys.path.append(os.path.join(LOCAL_DIRECTORY, "nodesAgent"))


PORT = 5006

from server import serve
import asyncio
import json
from kvStoreClient import KvStoreClient

from dhtNode import DhtNode, SimpleRemote, importDhtNodeDescriptor, exportDhtNodeDescriptor
from key import HashKey
from agentNode import Agent, Node,AdressHolder

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
        str(PORT), 
        0
    )
    
    Agent.register(localAgent)
    localNode.addAgent(localAgent.id)
    
    async def runJoin():
        print(localHashKey)
        # print(exportDhtNodeDescriptor(dhtNode))
        res = await KvStoreClient.getUpdatedDhtDescriptor("localhost:5005")
        print("joiging : \n", json.dumps(res["dhtNodeData"], indent=4))
        logicalNode = res["LogicalNode"]
        bootStrapRemote = SimpleRemote(logicalNode)        
        succDesc = await bootStrapRemote.findSuccessor(localHashKey.hashValue)
        # print("my successor: \n", json.dumps(succDesc, indent=4))
        # print(succDesc)
        
        succ = importDhtNodeDescriptor(succDesc)
        dhtPredOfSuccDesc = await bootStrapRemote.findSuccessor( DhtNode.get(succ)._predecessor.hashValue)
        # print(dhtPredOfSuccDesc)
        pred = importDhtNodeDescriptor(dhtPredOfSuccDesc)
        # print("my pred: \n", json.dumps(dhtPredOfSuccDesc, indent=4))
        
    
        dhtNode._successor = DhtNode.get(succ).id
        dhtNode._finger[0] = DhtNode.get(succ).id
        dhtNode._predecessor = DhtNode.get(pred).id 
               
               
        await dhtNode.update_neighbors()        
        await dhtNode.udpate_local_image(dhtNode._predecessor)
        print("me\n", json.dumps(exportDhtNodeDescriptor(dhtNode), indent=4))
        
        # print(DhtNode.get(dhtNode._successor))
        # print(Node.get(dhtNode._successor.hashValue))
        await dhtNode.udpate_local_image(dhtNode._successor)
        
    asyncio.run(runJoin()) 
    try:   
        asyncio.run(serve(PORT))
    except:
        print("oh no")
    
    