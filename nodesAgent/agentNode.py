from dataclasses import dataclass, field, asdict
from typing import List, Dict

class AdressHolder:
    agents = {}
    nodes = {}

@dataclass
class Agent:
    id: str
    ip: str
    port: str
    rank: int = -1
    capacity: int = 4000
    _hosting: str = ""
    
    
    ##########################
    @classmethod
    def fromDict(self, dict:Dict) -> 'Agent':
        ag = Agent(
            dict["id"], 
            dict["ip"], 
            dict["port"],
            dict["rank"], 
            dict["capacity"], 
            dict["_hosting"]
        )
        return ag
    
    @classmethod
    def importFromDict(self, dict:Dict) -> str:
        ag = Agent.fromDict(dict)
        Agent.register(ag)
        return ag.agent_id
    ##########################
    
    def toDict(self) -> Dict:
        return asdict(self)
    
    def hosting(self):
        if self._hosting != "":
            return 
    
    def show(self):
        print(f"agent: {self.id[:20]}, hosting node {Node.get(self._hosting).id[:20]}")
        
    def getAddr(self) -> str:
        return self.ip + ":" + self.port
        
        
@dataclass
class Node:
    id: str
    _agents: List[str] = field(default_factory=list, repr=False)
    
    #############################################################
    @classmethod
    def register(self, node:'Node') -> str:
        AdressHolder.nodes[node.id] = node
        return node.id
            
    @classmethod
    def get(self, node_id:str) -> 'Node':
        return AdressHolder.nodes.get(node_id, None)
    
    @classmethod
    def unlist(self, node_id:str) -> None:
        AdressHolder.nodes.pop(node_id, None)
    #############################################################
    @classmethod
    def fromDict(self, dict:Dict) -> 'Node':
        return Node(dict["id"])
    
    @classmethod
    def importFromDict(self, dict:Dict) -> str:
        node = Node.fromDict(dict)
        Node.register(node)
        for dc in dict["_agents"]:
            ag_id = Agent.importFromDict(dc)
            node.addAgent(Agent.get(ag_id))
            
        return node.Node_id
    #############################################################
    
    def toDict(self):
        dict = asdict(self)
        ags = self.agents()
        dict["_agents"] = [c.toDict() for c in ags.values()]
        return dict
    
    def agents(self) -> Dict[str, 'Agent']:
        output = {x: Agent.get(x) for x in self._agents}
        output = {k: v for k, v in output.items() if v is not None}
        return output
    
    def addAgent(self, agent_id: str) -> None:
        if not agent_id in self._agents:
            self._agents.append(agent_id)
            
    def delAgent(self, agent_id: str) -> None:
        if agent_id in self._agents:
            self._agents.remove(agent_id)
            
    def clearAgents(self) -> None:
        self._agents.clear()
    
    