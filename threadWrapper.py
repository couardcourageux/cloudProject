import os, sys
LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "dht"))
sys.path.append(os.path.join(LOCAL_DIRECTORY, "grpc"))



from dhtNode import DhtNode
from server import serve
from kvStoreClient import KvStoreClient



from key import HashKey

import asyncio

from multiprocessing import Process




async def killMultiple(wrappers):    
    await asyncio.gather(*[w.stop() for w in wrappers])

async def mapNetwork(wrappers, mainWrapper):
    await asyncio.gather(*[w.updateIdsInfos() for w in wrappers.values()])
    
    output = {}
    output[wrappers[mainWrapper].id] = wrappers[mainWrapper].export()
    for k, w in wrappers.items():
        if k != mainWrapper:
            output[w.id] = w.export()
    
    return output
    

def validateNetwork(network):
    output = []
    errors = []
    for n in network.values():
        output.append(n["id"])
        
    # print(network[output[0]])
        
    for idx, val in enumerate(output):
        # print(network[val])
        cd1, cd2, cd3 = False, False, False
        if idx == 0:
            cd1 = network[val]["predId"] == output[-1]
        else:
            cd1 = network[val]["predId"] == output[idx-1]
            
        if idx == len(output) - 1:
            cd2 = network[val]["precId"] == output[0]
        else:
            cd2 = network[val]["predId"] == output[idx+1]
        
        cd3 = network[val]["predId"] < network[val]["id"] \
                or (    
                    network[val]["predId"] == max(list(network.keys())) 
                    and network[val]["id"] == min(list(network.keys()))
                    )
        
        
        if not(cd1 and cd2 and cd3):
            errors.append(val[:10])
    
    for i in range(len(output)):
            output[i] = output[i][:10]
        
    
    return output, errors
            
        
        
        
            
    
    




def runThreaded(dhtNode, bootstrapAddr, port):
    localNode = dhtNode
    asyncio.run(localNode.join("localhost", str(port), bootstrapAddr))
    asyncio.run(serve(port))


class ThreadWrapper:
    
    def __init__(self, port:int, bootstrapAddr:str) -> None:
        self.port = port
        self.bootstrapAddr = bootstrapAddr
        self.dhtNode = DhtNode(True)
        self.dhtNode.generate_key()
        self.proc = None
        self.id = self.dhtNode.id.hashValue
        self.precId = None
        self.predid = None
        
    
        
    def run(self):
        self.proc = Process(target=runThreaded, args=(self.dhtNode, self.bootstrapAddr, self.port,))
        self.proc.start()
        # self.proc.join()
        
    def address(self):
        return "localhost:" + str(self.port)
    
    
    async def updateIdsInfos(self):
        res = await KvStoreClient.getUpdatedDhtDescriptor(self.address())
        res = res["dhtNodeData"]
        self.id = res["id"]
        self.precId = res["_successor"]
        self.predid = res["_predecessor"]
        
    async def stop(self):
        await KvStoreClient.plzDie(self.address())
        await asyncio.sleep(6)
        self.proc.join()
        
    def export(self):
        return {
            "id": self.id,
            "precId": self.precId,
            "predId": self.predid,
        }
        
        
        
    
        
