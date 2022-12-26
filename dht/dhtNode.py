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


import json

class DhtHolder:
    dhtNodes = {}
    localNodeHashVal = ""
    
    
    


@dataclass
class DhtNode:
    local: bool = False
    id: HashKey = None
    _predecessor: HashKey = field(default=None, repr=False)
    _successor: HashKey = field(default=None, repr=False)
    _finger: List[HashKey] = field(default_factory=list, repr=False)    
    # ces fonctions vont appeler une librairie logique, qui aura besoin de grpc, et des Nodes classiques
    
    #############################################
    @classmethod
    def register(self, dhtNode:'DhtNode') -> None:
        DhtHolder.dhtNodes[dhtNode.id.hashValue] = dhtNode
    
    @classmethod
    def get(self, dht_id: str | HashKey) -> 'DhtNode':
        dht_id_val = HashKey.getUsableHashVal(dht_id)
        return DhtHolder.dhtNodes.get(dht_id_val, None)
    
    @classmethod
    def getLocal(self):
        return DhtHolder.dhtNodes.get(DhtHolder.localNodeHashVal, None)
    
    def setLocal(self):
        DhtHolder.localNodeHashVal = self.id.hashValue
    
    @classmethod
    def unlist(self, dht_id: str | HashKey) -> None:
        if isinstance(dht_id, str):
            Node.unlist(dht_id)
        else:
            Node.unlist(dht_id.hashValue)
        DhtHolder.dhtNodes.pop(HashKey.getUsableHashVal(dht_id), None)
    ##############################################
    def toDict(self) -> dict:
        descriptor = asdict(self)
        descriptor["id"] = descriptor["id"].hashValue
        descriptor["_predecessor"] = descriptor["_predecessor"].hashValue
        descriptor["_successor"] = descriptor["_successor"].hashValue
        descriptor.pop("_finger", None)
        return descriptor
    
    @classmethod
    def fromDict(self, descriptor:dict) -> 'DhtNode':
        return DhtNode(
            descriptor["local"],
            HashKey(descriptor["id"], True),
            HashKey(descriptor["_predecessor"], True),
            HashKey(descriptor["_successor"], True),
        )
    ##############################################
    
    async def check_predecessor(self) -> bool:
        if self.local:
            predecessor_node = Node.get(self._predecessor.hashValue)
            return await LocalNodeLib.check_predecessor(predecessor_node)
            
        else:
            remote = SimpleRemote(exportDhtNodeDescriptor(self))
            await remote.check_predecessor()
    
        
    async def find_successor(self, hashKey:str | HashKey, withNeighbors=False):
        """return the descriptor of the DhtNode responsible for the key

        :param  hashKey 
        :return dict : _description_ of the responsible DhtNode
        """
        # for c, v in DhtHolder.dhtNodes.items():
        #     if c != DhtHolder.localNodeHashVal:
        #         print(json.dumps(exportDhtNodeDescriptor(v), indent=4))
                
                
        if self.local:
            id_val = HashKey.getHashKeyClean(hashKey)
            intervals = [self._predecessor, self.id] + list(filter(lambda x: isinstance(x, HashKey),self._finger))
            guardians = id_val.findClosestsGuardians(intervals)
            # print("intervals\n", intervals)
            # print("guardians\n", guardians)
            if guardians["closest_succ_known"] == self.id:
                dhtNodeData = exportDhtNodeDescriptor(self)
                if withNeighbors:
                    predNode = DhtNode.get(self._predecessor)
                    succNode = DhtNode.get(self._successor)
                    
                    dhtNodeData["predDhtNode"] = predNode.toDict()
                    dhtNodeData["succDhtNode"] = succNode.toDict()
                    
                return dhtNodeData
            
            
            elif guardians["closest_succ_known"] == self._successor:
                dhtNodeData = exportDhtNodeDescriptor(DhtNode.get(self._successor))
                
                if  withNeighbors:
                    dhtNodeData["predDhtNode"] = self.toDict() 
                    dhtNodeData["succDhtNode"] = self.find_successor(DhtNode.get(self._successor)._successor)
                return dhtNodeData
            else:
                remote = DhtNode.get(guardians["closest_pred_known"])
                return await remote.find_successor(id_val, withNeighbors)
        
        else:
            remote = Node.get(self.id.hashValue)
            if isinstance(hashKey, HashKey):
                searched = hashKey.hashValue
            else:
                searched = hashKey
                
            return await LocalNodeLib.find_successor(searched, remote, withNeighbors)

    
    def _fix_finger(self, finger_id:str):
        remoteNode = DhtNode.get(self._finger[finger_id])
        # await ping
        ping_resp = True
        if ping_resp:
            # await description
            pass
    
    def generate_key(self):
        if self.local:
            self.id = HashKey.getRandom()

    
    def init_finger_table(self):
        pass

    def init_successor_list(self, successor_hash_id:str):
        pass
    
    async def join(self, localAddr:str, localPort:str, bootstrap_addr:str):
        localHashKey = self.id
        self.local = True
        self._predecessor = localHashKey
        self._successor = localHashKey
        self._finger = [None for i in range(256)]
        self._finger[0] = localHashKey
        
        
        
        DhtNode.register(self)
        self.setLocal()
        
    
        
        localNode = Node(localHashKey.hashValue)
        Node.register(localNode)
        
        localAgent = Agent(
            HashKey.getRandom().value,
            localAddr,
            localPort,
            0
        )
        Agent.register(localAgent)
        localNode.addAgent(localAgent.id)
        
        if bootstrap_addr:
            res = await KvStoreClient.getUpdatedDhtDescriptor(bootstrap_addr)
            logicalNode = res["LogicalNode"]
            bootStrapRemote = SimpleRemote(logicalNode)        
            succDesc = await bootStrapRemote.findSuccessor(localHashKey.hashValue)
        
            succ = importDhtNodeDescriptor(succDesc)
            dhtPredOfSuccDesc = await bootStrapRemote.findSuccessor( DhtNode.get(succ)._predecessor.hashValue)
            pred = importDhtNodeDescriptor(dhtPredOfSuccDesc)

            self._successor = DhtNode.get(succ).id
            self._finger[0] = DhtNode.get(succ).id
            self._predecessor = DhtNode.get(pred).id      
            
            
            await self.update_neighbors()        
            await self.udpate_local_image(self._predecessor)  
            await self.udpate_local_image(self._successor)
        
    
    def stabilize(self):
        if self.local:
            mySucc = DhtNode.get(self._successor)
            node_interDesc = self.find_successor(mySucc._predecessor)
            if node_interDesc:
                if mySucc._predecessor == self.id:
                    return
                if self.id == self._successor \
                    or HashKey(node_interDesc["dhtNodeData"]["id"]).is_inside(self.id, self._successor):
                    node_inter = importDhtNodeDescriptor(node_interDesc)
                    self._successor = node_inter.id
            if self._successor != self.id:
                mySucc.notify_new_pred(exportDhtNodeDescriptor(self))

    
    async def notify_new_pred(self, newPredDescFull:dict):
        if self.local:
            newPred = DhtNode.get(importDhtNodeDescriptor(newPredDescFull))
            if not self._predecessor \
                or newPred.id.is_inside(self._predecessor, self.id):
                    self._predecessor = newPred.id

        else:
            remote = Node.get(self.id.hashValue)
            await LocalNodeLib.notify_new_predecessor(newPredDescFull, remote)


    async def update_neighbors(self):
        if self.local:
            dhtPred = DhtNode.get(self._predecessor)
            dhtSucc = DhtNode.get(self._successor)
            selfDescriptor = exportDhtNodeDescriptor(self)
            await dhtPred.update_successor(selfDescriptor)
            await dhtSucc.update_predecessor(selfDescriptor)
    
    @classmethod
    async def udpate_local_image(self, hashKey:HashKey):
        dhtNode = DhtNode.get(hashKey)
        if not dhtNode.local:
            result = await dhtNode.getUpdatedDescriptor()
            importDhtNodeDescriptor(result)
            
    
    async def getUpdatedDescriptor(self):
           return await LocalNodeLib.getUpdatedDescriptor(Node.get(self.id.hashValue))
    
    async def update_others(self):
        if self.local:
            for i in range(256):
                predKey = self.id.subint(2**i)
                predNodeDescriptor = await self.find_successor(predKey)
                remote = SimpleRemote(predNodeDescriptor["LogicalNode"])
                await remote._update_finger_table(exportDhtNodeDescriptor(self), i)
            
    
    async def _update_finger_table(self, callingNodeDescriptorFull:dict, i:int) -> None:
        if self.local:
            distantDhtNode = DhtNode.fromDict(callingNodeDescriptorFull["dhtNodeData"])
            if distantDhtNode.id == self.id:
                return 
            DhtNode.register(distantDhtNode)
            Node.importFromDict(callingNodeDescriptorFull["LogicalNode"])
            
            Node.unlist(self._finger[i].hashValue)
            self._finger[i] = distantDhtNode.id
        else:
            
            remote = Node.get(self.id.hashValue)
            await LocalNodeLib.updateFingerTable(callingNodeDescriptorFull, i, remote)
                    

    async def update_successor(self, callingNodeDescriptorFull:dict):
        if self.local:
            distantNodeHashVal = importDhtNodeDescriptor(callingNodeDescriptorFull)
            self._successor = HashKey(distantNodeHashVal, True)
            self._finger[0] = HashKey(distantNodeHashVal, True)
            # print("successor updated by ", distantNodeHashVal, "\n", json.dumps(exportDhtNodeDescriptor(self)["dhtNodeData"], indent=4))
            return
        else:
            remote = Node.get(self.id.hashValue)               
            await LocalNodeLib.updateSuccessor(callingNodeDescriptorFull, remote)
            return 
            
    
    async def update_predecessor(self, callingNodeDescriptorFull:dict):
        if self.local:
            distantNodeHashVal = importDhtNodeDescriptor(callingNodeDescriptorFull)
            self._predecessor = HashKey(distantNodeHashVal, True)
            # print("predecessor updatedby ", distantNodeHashVal, "\n", json.dumps(exportDhtNodeDescriptor(self)["dhtNodeData"], indent=4))

            return
        else:
            remote = Node.get(self.id.hashValue)               
            await LocalNodeLib.updatePredecessor(callingNodeDescriptorFull, remote)
            return 

    def update_successor_list(self):
        pass



class SimpleRemote:
    
    def __init__(self, logicalNodeDescriptor:dict) -> None:
        self.logicalNode = Node.get(Node.importFromDict(logicalNodeDescriptor))
        
    async def findSuccessor(self, hashKey:str):
 
        return await LocalNodeLib.find_successor(hashKey, self.logicalNode)
        
    async def _update_finger_table(self, callingNodeDescriptorFull:dict, i:int) -> None:
        await LocalNodeLib.updateFingerTable(callingNodeDescriptorFull, i, self.logicalNode)
        pass
    
    async def check_predecessor(self):
        await LocalNodeLib.make_check_predecessor(DhtNode.get(self._predecessor))        
        
    def close(self):
        Node.unlist(self.logicalNode.id)
        
    def __del__(self) -> None:
        self.close()    
        
        




def exportDhtNodeDescriptor(dhtNode:DhtNode) -> dict:
    node = Node.get(dhtNode.id.hashValue)
    return {
        "dhtNodeData":dhtNode.toDict(),
        "LogicalNode": node.toDict()
    }

def importDhtNodeDescriptor(descriptor:dict, localOverride=False) -> str:
    dhtDesc = descriptor["dhtNodeData"]
    nodeDesc = descriptor["LogicalNode"]
    
    dhtDesc["local"] = localOverride
    dhtNode = DhtNode.fromDict(dhtDesc)
    DhtNode.register(dhtNode)
    if localOverride:
        dhtNode.setLocal()
    
    return Node.importFromDict(nodeDesc)
    
    
    
    