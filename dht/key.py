import secrets
import hashlib

from typing import Union
        
    
class HashKey:
    def __init__(self, value:str) -> None:
        self.value = value
        self.hashValue = self.hash()
        
    @classmethod
    def getRandom(self) -> 'HashKey':
        return HashKey(secrets.token_hex(256))
    
    def setValue(self, value: str, hashValue:str) -> None:
        self.value = value
        self.hashValue = hashValue
        
    def updateValue(self, newValue:str) -> None:
        self.value = newValue
        self.hashValue = self.hash()
        
    def hash(self):
        return hashlib.sha256(str.encode(self.value)).hexdigest()
    
    def sumint(self, value:Union[int, str, 'HashKey']) -> str:
        if isinstance(value, int):
            val = value
        elif isinstance(value, str):
            val = int(value, 16)
        elif isinstance(value, HashKey):
            val = int(value.hashValue, 16)
        else:
            print(value)
            raise TypeError     
        
        res = (int(self.value, 16) + val) % pow(2, 256)
        return self.canonicalize(res)
    
    def subint(self, value: Union[int, str, 'HashKey']) -> str:
        if isinstance(value, int):
            val = value
        elif isinstance(value, str):
            val = int(value, 16)
        elif isinstance(value, HashKey):
            val = int(value.hashValue, 16)
        else:
            print(value)
            raise TypeError    
        
        res = (int(self.value, 16) - val) % pow(2, 256)
        return self.canonicalize(res) 
        
    
    @classmethod
    def canonicalize(self, value:str) -> str:
        return format(int(value, 16), '0>{}x'.format(256 // 4))
    
    def is_inside(self, limit1:'HashKey', limit2:'HashKey') -> bool:
        """true if self @ ]limit1, limit2[

        :param HashKey limit1
        :param HashKey limit2
        :return bool
        """
        return self > limit1 and self < limit2
    
    def is_between_r_inclus(self, limit1:'HashKey', limit2:'HashKey') -> bool:
        """true if self @ ]limit1, limit2]

        :param HashKey limit1
        :param HashKey limit2
        :return bool
        """
        return (self == limit2 and self != limit1) or self.is_inside(limit1, limit2)
    
    def is_between_l_inclus(self, limit1:'HashKey', limit2:'HashKey') -> bool:
        """true if self @ [limit1, limit2[

        :param HashKey limit1
        :param HashKey limit2
        :return bool
        """
        return (self != limit2 and self == limit1 ) or self.is_inside(limit1, limit2) 
    
    def is_between_l_inclus(self, limit1:'HashKey', limit2:'HashKey') -> bool:
        """true if self @ [limit1, limit2]

        :param HashKey limit1
        :param HashKey limit2
        :return bool
        """
        return (self == limit2 or self == limit1) or self.is_inside(limit1, limit2)

     
    
    
    
    def __repr__(self) -> str:
        return self.value[:5] + ".. ; " + self.hashValue[:15] + ".."
    
    def __gt__(self, otherKey:'HashKey') -> bool:
        return self.hashValue > otherKey.hashValue
    
    def __ge__(self, otherKey:'HashKey') -> bool:
        return self.hashValue >= otherKey.hashValue
    
    def __eq__(self, otherKey:Union[str, 'HashKey']) -> bool:
        if isinstance(otherKey, str):
            return self.hashValue == otherKey
        elif isinstance(otherKey, HashKey):
            return self.hashValue == otherKey.hashValue
    
    def __le__(self, otherKey:'HashKey') -> bool:
        return self.hashValue <= otherKey.hashValue
    
    def __lt__(self, otherKey:'HashKey') -> bool:
        return self.hashValue < otherKey.hashValue
    
    def __ne__(self, otherKey:'HashKey') -> bool:
        return self.hashValue != otherKey.hashValue
    
    def __add__(self, value: Union[int, str, 'HashKey']) -> str:
        if isinstance(value, int):
            val = value
        elif isinstance(value, str):
            val = int(value, 16)
        elif isinstance(value, HashKey):
            val = int(value.hashValue, 16)
        else:
            print(value)
            raise TypeError     
        
        return self.sumint(val)
    
    def __sub__(self, value: Union[int, str, 'HashKey']) -> str:
        if isinstance(value, int):
            val = value
        elif isinstance(value, str):
            val = int(value, 16)
        elif isinstance(value, HashKey):
            val = int(value.hashValue, 16)
        else:
            print(value)
            raise TypeError     
        
        return self.subint(val)
    
    
if __name__ == '__main__':
    pass
    