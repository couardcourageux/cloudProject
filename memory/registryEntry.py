from dataclasses import dataclass, field
import time


@dataclass # il faudra implémenter ce qu'il faut pour le freeze
class RegisterEntry:
    key: str
    value: str
    
    nb_modifs: int = field(init=False)
    nb_requests: int = field(init=False)
    
    author_id: str
    c_timestamp: float = field(init=False)
    m_timestamp: float = field(init=False)
   
    
    public_read: bool = False
    public_write: bool = False
    modifier_id: str = field(init=False)
    
    def __post_init__(self):
        self.c_timestamp = time.time()
        self.m_timestamp = None
        self.nb_modifs = 0
        self.nb_requests = 0
        self.modifier_id = None
    
    def grantAccess(self, user_id: str) -> bool:
        test = self.public_read or self.author_id == user_id
        if test:
            self.nb_requests += 1
        return test
    
    def modify(self, value:str, user_id:str) -> None:
        self.value = value
        self.nb_modifs += 1
        self.modifier_id = user_id
        self.m_timestamp = time.time()