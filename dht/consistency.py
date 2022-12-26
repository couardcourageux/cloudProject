import os, sys

from kvStoreClient import KvStoreClient

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "nodesAgent"))

from dataclasses import dataclass, field, asdict
from typing import List, Dict

from agentNode import Node, AdressHolder, Agent
from key import HashKey

from localNodeLib import LocalNodeLib
from distantNodeLib import DistantNodeLib

from dhtNode import DhtNode, importDhtNodeDescriptor, exportDhtNodeDescriptor

import json
import asyncio

async def getUpdatedPred(dhtNode:DhtNode):
    predNode = DhtNode.get(dhtNode._predecessor)
    if await predNode._is_alive():
        try:
            await DhtNode.udpate_local_image(dhtNode._predecessor)
        except:
            temp = await dhtNode.find_successor(predNode._predecessor)
            dhtNode._predecessor = importDhtNodeDescriptor(temp)
    else:
        temp = await dhtNode.find_successor(predNode._predecessor)
        dhtNode._predecessor = importDhtNodeDescriptor(temp)
    
async def getUpdatedSucc(dhtNode:DhtNode):
    succNode = DhtNode.get(dhtNode._successor)
    if await succNode._is_alive():
        try:
            await DhtNode.udpate_local_image(dhtNode._successor)
        except:
            pass
    else:
        for n in dhtNode._backupSuccessors:
            if n != None:
                closest = DhtNode.get(n)
                if await closest._is_alive():
                    dhtNode._successor = n
                    dhtNode._finger[0] = n
                    await getUpdatedSucc(dhtNode)
                    break
        dhtNode._successor = None
        dhtNode._finger[0] = None

async def getUpdatedNeighbors(dhtNode: DhtNode):
    await asyncio.gather(getUpdatedPred(dhtNode), getUpdatedSucc(dhtNode))
    
    
    
        
async def updateFingers(dhtNode: DhtNode):
    for idx, f in enumerate(dhtNode._finger):
        if not isinstance(f, type(None)):
            finger = DhtNode.get(f)
            if await finger._is_alive():
                try:
                    await DhtNode.udpate_local_image(f)
                except:
                    dhtNode._finger[idx] = None
    
    
async def ensure_consistency(dhtNode):
    # await getUpdatedNeighbors(dhtNode)
    # await updateFingers(dhtNode)
    # await dhtNode.update_others()
    # succ = DhtNode.get(dhtNode._successor)
    # await dhtNode.stabilize()
    
    pass
    