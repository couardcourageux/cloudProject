
from dataclasses import dataclass
from typing import Tuple


class KeyNotFound(Exception):
    """Used to specify that there is no entry for this key

    :param str Exception: the key in question
    """
    
    def __init__(self, key: str) -> None:
        self.key = key
        self.message = f"key {self.key} not found"
        super().__init__(self.message)
        
class UnauthorizedReading(Exception):
    """Used to specify that the user cannot access this entry

    :param str Exception: the key in question
    :param indent Exception: the the user id
    """
    def __init__(self, inf:Tuple[str, str]) -> None:
        self.key = inf[0]
        self.id = inf[1]
        self.message = f"user {self.id} have no read access over the key {self.key}"
        super().__init__(self.message)
        
class UnauthorizedWriting(Exception):
    """Used to specify that the user cannot write this entry

    :param str Exception: the key in question
    :param indent Exception: the the user id
    """
    def __init__(self, inf:Tuple[str, str]) -> None:
        self.key = inf[0]
        self.id = inf[1]
        self.message = f"user {self.id} have no write access over the key {self.key}"
        super().__init__(self.message)

