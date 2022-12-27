from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import typing


from registryEntry import RegisterEntry
from DBerrors import KeyNotFound, UnauthorizedReading, UnauthorizedWriting





@dataclass
class CustomrResp:
    status: int
    data: 'typing.any'=None
    errors: List[Exception] = field(default_factory=list)



class MockDatabase:
    
    __data = {}
    __size = 0
    
    
    @classmethod
    def refresh_size(self):
        self.__size = len(self.__data.keys())
    
    @classmethod
    @property
    def size(self):
        return self.__size
    
    
    @classmethod
    def getEntry(self, key: str, user_id:str) -> CustomrResp:
        
        entry = self.__data.get(key, None)
        if  entry is None:
            return CustomrResp(status=1, 
                            data=f"{key} not found", 
                            errors=[KeyNotFound(key)]
                            )
        
        if entry.grantAccess(user_id):
            return CustomrResp(status=0, 
                            data=entry, 
                            )
        else:
            return CustomrResp(status=1, 
                            data=f"you have no authorisation over {key}", 
                            errors=[UnauthorizedReading((key, user_id))]
                            )
    
    
    @classmethod
    def setEntry(self, key:str, value:str, user_id:str, rights:Tuple[int, int]=(0, 0)) -> CustomrResp:
        entry = self.__data.get(key, None)
        if entry is None:
            entry = RegisterEntry(key, value, user_id, rights[0], rights[1])
            self.__data[key] = entry
            self.__size += 1
            
        else:
            if entry.public_write:
                entry.modify(value, user_id)
                self.__data[key] = entry
            else:
                if entry.author_id == user_id:
                    entry.modify(value, user_id)
                    self.__data[key] = entry
                else:
                    return CustomrResp(status=1, data=f"{key} failed to be added", errors=[UnauthorizedWriting((key, user_id))])
        return CustomrResp(status=0, data=f"{key} successfully added")
    
    @classmethod
    def popEntry(self, key:str, user_id:str) -> CustomrResp:
        entry = self.__data.get(key, None)
        if entry is None:
            return CustomrResp(status=1, data=f"{key} not found", errors=[KeyNotFound(key)])
            
        else:
            if entry.public_write:
                del self.__data[key]
                self.__size -= 1
            else:
                if entry.author_id == user_id:
                    del self.__data[key]
                    self.__size -= 1
                else:
                    return CustomrResp(status=1, data=f"{key} failed to be deleted", errors=[UnauthorizedWriting((key, user_id))])
        return CustomrResp(status=0, data=f"{key} successfully deleted")
        
        
