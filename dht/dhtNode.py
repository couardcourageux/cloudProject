import os, sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "nodesAgent"))

from dataclasses import dataclass, field, asdict
from typing import List, Dict

from agentNode import Node, AdressHolder, Agent
from key import HashKey

from localNodeLib import LocalNodeLib
from distantNodeLib import DistantNodeLib


@dataclass
class Successor:
    _successor: HashKey = field(default=None, repr=False)
    _finger: List[HashKey] = field(default_factory=list, repr=False)
    


@dataclass
class DhtNode:
    local: bool = False
    id: HashKey = None
    _predecessor: HashKey = field(default=None, repr=False)
    _Successor: Successor = field(default_factory=Successor, repr=False)
    
    # ces fonctions vont appeler une librairie logique, qui aura besoin de grpc, et des Nodes classiques
    
    async def check_predecessor(self) -> bool:
        if self.local:
            predecessor_node = Node.get(self._predecessor.hashValue)
            return await LocalNodeLib.check_predecessor(predecessor_node)
            
        # else:
        #     dht_node_repr = Node.get(self.id.hashValue)
        #     DistantNodeLib.check_predecessor(dht_node_repr)
        # pass
    
    def find_successor(self, hash_id:str):
        pass
        
    def _find_successor_rec(self, hash_id:str):
        pass
    
    def _fix_finger(self, finger_id:str):
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
