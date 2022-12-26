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
        
        
        
    
        
