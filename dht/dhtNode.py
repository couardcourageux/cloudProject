import os, sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "nodesAgent"))

from dataclasses import dataclass, field, asdict
from typing import List, Dict

from agentNode import Node, AdressHolder, Agent
from key import HashKey

from localNodeLib import LocalNodeLib
from distantNodeLib import DistantNodeLib


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
        if self.local:
            id_val = HashKey.getHashKeyClean(hashKey)
            intervals = [self._predecessor, self.id] + list(filter(lambda x: isinstance(x, HashKey),self._finger))
            guardians = id_val.findClosestsGuardians(intervals)
            
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
                print("else")
                remote = DhtNode.get(guardians["closest_pred_known"])
                return await remote.find_successor(id_val, withNeighbors)
        
        else:
            print("remote call")
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
    
    def join(self, node_id:str, node_addr:str, bootstrap_addr:str):
        pass
    
    def stabilize(self):
        pass

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
        # print(exportDhtNodeDescriptor(dhtNode))
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
            return
        else:
            remote = Node.get(self.id.hashValue)               
            await LocalNodeLib.updateSuccessor(callingNodeDescriptorFull, remote)
            return 
            
    
    async def update_predecessor(self, callingNodeDescriptorFull:dict):
        if self.local:
            distantNodeHashVal = importDhtNodeDescriptor(callingNodeDescriptorFull)
            self._predecessor = HashKey(distantNodeHashVal, True)
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
        print(hashKey)
        truc = await LocalNodeLib.find_successor(hashKey, self.logicalNode)
        print(truc)
        return truc
        
    async def _update_finger_table(self, callingNodeDescriptorFull:dict, i:int) -> None:
        # rpc call to agents of _update_finger_table
        pass
    
    async def check_predecessor(self):
        await LocalNodeLib.make_check_predecessor(self.logicalNode)        
        
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
    
    
    
    