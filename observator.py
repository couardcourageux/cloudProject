import os
import sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "grpc"))
sys.path.append(os.path.join(LOCAL_DIRECTORY, "dht"))
sys.path.append(os.path.join(LOCAL_DIRECTORY, "nodesAgent"))


from server import serve
import asyncio

from kvStoreClient import KvStoreClient





async def run(port):
    print( await KvStoreClient.getUpdatedDhtDescriptor("localhost:{}".format(port)))
    
    
if __name__ == "__main__":
    # for i in range(5006, 5009):
    asyncio.run(run(5005))