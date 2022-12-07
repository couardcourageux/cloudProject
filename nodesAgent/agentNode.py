from dataclasses import dataclass, field, asdict
from typing import List, Dict

class AdressHolder:
    agents = {}
    nodes = {}
    local_agent_id = ""
    
    @classmethod
    def get_local_agent(self) -> str:
        return self.local_agent_id
    @classmethod
    def set_local_agent(self, agent_id:str) -> None:
        self.local_agent_id = agent_id

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
    @classmethod
    def register(self, agent:'Agent') -> None:
        AdressHolder.agents[agent.agent_id] = agent
            
    @classmethod
    def get(self, agent_id:str) -> 'Agent':
        return AdressHolder.agents.get(agent_id, None)
    
    @classmethod
    def unlist(self, agent_id:str) -> None:
        AdressHolder.agents.pop(agent_id, None)
    #################################################
    
    def toDict(self) -> Dict:
        return asdict(self)
    
    def hosting(self):
        if self._hosting == "":
            return None
        return Node.get(self._hosting) 
    
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
        sortedAgents = sorted(self.agents, key=lambda a: a.rank)
        output = {x: Agent.get(x) for x in sortedAgents if x.rank >= 0}
        output = {k: v for k, v in output.items() if v is not None}
        return output
    
    def getAgentsIterator(self) -> 'NodeIteratorOverAgents':
        return NodeIteratorOverAgents(self)
    
    def addAgent(self, agent_id: str) -> None:
        if not agent_id in self._agents:
            self._agents.append(agent_id)
            
    def delAgent(self, agent_id: str) -> None:
        if agent_id in self._agents:
            self._agents.remove(agent_id)
            
    def clearAgents(self) -> None:
        self._agents.clear()
    
class NodeIteratorOverAgents:
    def __init__(self, node:Node) -> None:
        self.agents = list(node.agents())
        self.current = 0
        self.limit = len(self.agents) 
        
    def hasNext(self) -> bool:
        return self.current < self.limit
        
    def next(self) -> Agent:
        if self.hasNext():
            ag = Agent.get(self.agents[self.current])
            self.current += 1
            return ag
    