import os, sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "grpc"))



from dhtNode import DhtNode
from signalHandler import SignalHandler

import asyncio


async def stabilize():
    while SignalHandler.running():
        await asyncio.sleep(5)
        localNode = DhtNode.getLocal()
        await localNode.stabilize()
        
        
        
async def checkPred():
    while SignalHandler.running():
        await asyncio.sleep(3)
        localNode = DhtNode.getLocal()
        await localNode.check_predecessor()
        

async def updateMyPointers():
    while SignalHandler.running():
        await asyncio.sleep(10)
        localNode = DhtNode.getLocal()
        await localNode.update_others()
        
async def updateMyNeighbors():
    while SignalHandler.running():
        await asyncio.sleep(30)
        localNode = DhtNode.getLocal()
        await localNode.update_neighbors()


async def serveCronJobs():
    await asyncio.gather(stabilize(), checkPred(), updateMyPointers(), updateMyNeighbors())