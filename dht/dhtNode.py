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
        descriptor.pop("_finger", None)
        return descriptor
    
    @classmethod
    def fromDict(self, descriptor:dict) -> 'DhtNode':
        return DhtNode(
            descriptor["local"],
            HashKey(descriptor["id"], True),
            descriptor["_predecessor"],
            descriptor["_successor"]
        )
    ##############################################
    
    async def check_predecessor(self) -> bool:
        if self.local:
            predecessor_node = Node.get(self._predecessor.hashValue)
            return await LocalNodeLib.check_predecessor(predecessor_node)
            
        # else:
        #     dht_node_repr = Node.get(self.id.hashValue)
        #     DistantNodeLib.check_predecessor(dht_node_repr)
        # pass
    
        
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
                    
                # describe self
                return dhtNodeData
            
            
            if guardians["closest_succ_known"] == self._successor:
                dhtNodeData = exportDhtNodeDescriptor(DhtNode.get(self._successor))
                if not withNeighbors:
                    return exportDhtNodeDescriptor(dhtNodeData)
                else:
                    # remoteCall
                    #describe successor
                    return
            else:
                remote = DhtNode.get(guardians["closest_pred_known"])
                return await remote.find_successor(id_val)
        
        else:
            # on appelle la remote via grpc
            return

    
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
            return
            
    
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
        return
        

    async def update_successor(self, callingNodeDescriptorFull:dict):
        if self.local:
            distantDhtNode = DhtNode.fromDict(callingNodeDescriptorFull["dhtNodeData"])
            DhtNode.register(distantDhtNode)
            Node.importFromDict(callingNodeDescriptorFull["LogicalNode"])
            self._successor = distantDhtNode.id
            self._finger[0] = distantDhtNode.id
            return
        else:
            # call grpc method to update
            return
    
    async def update_predecessor(self, callingNodeDescriptorFull:dict):
        if self.local:
            distantDhtNode = DhtNode.fromDict(callingNodeDescriptorFull["dhtNodeData"])
            DhtNode.register(distantDhtNode)
            Node.importFromDict(callingNodeDescriptorFull["LogicalNode"])
            DhtNode.unlist(self._predecessor)
            self._predecessor = distantDhtNode.id
            return
        else:
            # call grpc method to update
            return

    def update_successor_list(self):
        pass



class SimpleRemote:
    
    def __init__(self, logicalNodeDescriptor:dict) -> None:
        self.logicalNode = Node.importFromDict(logicalNodeDescriptor)
        
    async def _update_finger_table(self, callingNodeDescriptorFull:dict, i:int) -> None:
        # rpc call to agents of _update_finger_table
        pass
        
    def close(self):
        Node.unlist(self.logicalNode.id)
        
    def __del__(self) -> None:
        self.close()    
        
        




def exportDhtNodeDescriptor(dhtNode:DhtNode) -> dict:
    return {
        "dhtNodeData":dhtNode.toDict(),
        "LogicalNode": Node.get(dhtNode.id.hashValue).toDict()
    }