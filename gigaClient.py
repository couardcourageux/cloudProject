import os
import sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "grpc"))

import asyncio

from kvStoreClient import KvStoreClient

async def loopingId():
    while True:
        await KvStoreClient.join_network("localhost:5000")
        print("resp received id")
        
async def loopingNode():
    while True:
        await KvStoreClient.searchNode("localhost:5000", 'tamere')
        print("resp received Node")
        
async def loop_run():
    await asyncio.gather(loopingId(), loopingNode())
    
async def run():
    # await KvStoreClient.join_network("localhost:5000")
    await KvStoreClient.searchNode("localhost:5000", 'tamere')
    
if __name__ == "__main__":
    asyncio.run(loop_run())
    # asyncio.run(run())