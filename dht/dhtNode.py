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
    def unlist(self, dht_id: str | HashKey) -> None:
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
            descriptor["id"],
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
    
    async def find_successor(self, hash_id:str):
        pass
        
    async def _find_successor_rec(self, hashKey:str | HashKey, withNeighbors=False):
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
                return await remote._find_successor_rec(id_val)
        
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

    def get_closest_preceding_finger(self, hash_id:str):
        pass
    
    def init_finger_table(self):
        pass

    def init_successor_list(self, successor_hash_id:str):
        pass
    
    def join(self, node_id:str, node_addr:str, bootstrap_addr:str):
        pass
    
    def stabilize(self):
        pass

    def update_neighbors(self):
        pass
    
    def update_others(self):
        pass

    def update_successor(self):
        pass

    def update_successor_list(self):
        pass








def exportDhtNodeDescriptor(dhtNode:DhtNode) -> dict:
    return {
        "dhtNodeData":dhtNode.toDict(),
        "LogicalNode": Node.get(dhtNode.id.hashValue).toDict()
    }