from agentNode import  NodeIteratorOverAgents

import grpc

# def decodecorator(per_addr=2, n_addr=-1):
#     def decorator(func):
#         def wrapper_func(*args, **kwargs):
#             #here is it to place the logic of the wrapper
        
#             print(per_addr, n_addr, "wrapper")
#             func(*args, **kwargs)
        
#         return wrapper_func
#     return decorator

class ConnectionNotFoundException(Exception):
    def __init__(self, key: str) -> None:
        self.key = key
        self.message = f"connection not found to node {key[:15]}"
        super().__init__(self.message)
    


def decoTryConnection(nodeIterator:NodeIteratorOverAgents,
                      n_addr:int=2,
                      per_addr:int=2, 
                    ):
    def try_connection(func):
        async def wrapper_func(*args, **kwargs):
            if n_addr == - 1:
                while nodeIterator.hasNext():
                    count = 0
                    while count < per_addr:
                        try:
                            return await func(*args, distantAgentHost=nodeIterator.getNext().getAddr(), **kwargs)
                        except grpc.RpcError as err:
                            print(f"{err=}, {type(err)=}")
                            count += 1
                raise ConnectionNotFoundException("to change")
            else :
                ext_count = 0
                while ext_count < n_addr:
                    count = 0
                    while count < per_addr:
                        try:
                            return await func(*args, distantAgentHost=nodeIterator.getNext().getAddr(), **kwargs)
                        except grpc.RpcError as err:
                            print(f"{err=}, {type(err)=}")
                            count += 1
                    ext_count += 1
                raise ConnectionNotFoundException("to change")
                        
            return 
        return wrapper_func
    return try_connection