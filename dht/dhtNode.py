import os, sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "nodesAgent"))

from dataclasses import dataclass, field, asdict
from typing import List, Dict

from agentNode import Node, AdressHolder, Agent

class DhtNodeHolder:
    dhtNodes = {}

@dataclass
class Successor:
    _successor: str = field(default="", repr=False)
    _finger: List[str] = field(default_factory=list, repr=False)
    


@dataclass
class DhtNode:
    nodeId: str = ""
    rank: int = -1
    _predecessor: str = field(default="", repr=False)
    _Successor: Successor = field(default_factory=Successor, repr=False)
    
    # ces fonctions vont appeler une librairie logique, qui aura besoin de grpc, et des Nodes classiques
    
    def check_predecessor(self):
        pass
    
    def find_successor(self, hash_id:str):
        pass
        
    def _find_successor_rec(self, hash_id:str):
        pass
    
    def _fix_finger(self, finger_id:str):
        pass
    
    def generate_key(self):
        pass

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
