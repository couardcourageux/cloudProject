import secrets
import hashlib

from typing import Union, List
        

    
class HashKey:
    

    
    def __init__(self, value:str, fromHash=False) -> None:
        if fromHash:
            self.value = value
            self.hashValue = value
        else:
            self.value = value
            self.hashValue = self.hash()
        
    @classmethod
    def getUsableHashVal(self, value: Union[str, 'HashKey']) -> str:
        if isinstance(value, str):
            return value
        
        return value.hashValue
        
    @classmethod
    def getHashKeyClean(self, value:Union[str, 'HashKey']) -> 'HashKey':
        if isinstance(value, str):
            return HashKey(value, fromHash=True)
        return value
        
        
    @classmethod
    def getRandom(self) -> 'HashKey':
        return HashKey(secrets.token_hex(256))
    
    @classmethod
    def fromInt(self, val:int) -> 'HashKey':
        stringVal = format(val, '0>{}x'.format(256 // 4))
        return HashKey(stringVal, True)
    
    def toInt(self) -> int:
        return int(self.hashValue, 16)
    
    
    def findClosestsGuardians(self, keys:List['HashKey']) -> dict:
        if len(keys) == 3 and keys[0] == keys[1] and keys[1] == keys[2]:
            return {
                    "closest_pred_known":keys[0],
                    "closest_succ_known":keys[0], 
                }
        for i in range(-1, len(keys) - 1):
            if self.is_between_r_inclus(keys[i], keys[i+1]):
                return {
                    "closest_pred_known":keys[i],
                    "closest_succ_known":keys[i+1], 
                }
    
    
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
        if limit1 > limit2:
            return self > limit2 or self < limit1
        
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
    
    def is_between_all_inclus(self, limit1:'HashKey', limit2:'HashKey') -> bool:
        """true if self @ [limit1, limit2]

        :param HashKey limit1
        :param HashKey limit2
        :return bool
        """
        return (self == limit2 or self == limit1) or self.is_inside(limit1, limit2)

    def __repr__(self) -> str:
        return self.hashValue
    
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
    
    # keys = []
    # keys.append(HashKey(2**256, True))
    # print(keys[0].hashValue in keys)
    # print(len(keys[0].hashValue))
    
    # keys = [HashKey.getRandom() for i in range(4)]
    # keys.sort()
    # print(keys)
    # print()
    # print(key.subint(1))
    # print(len(format(2**256, '0>{}x'.format(256 // 4))))

    
    pass
    