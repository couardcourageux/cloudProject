def decoTryConnection(nodeIterator:str,
                      per_addr:int=2, 
                      n_addr:int=2
                    ):
    def try_connection(func):
        def wrapper_func(*args, **kwargs):
            result = None
            result =  func(*args, distantHost=nodeIterator, **kwargs)
                    
            return result
        return wrapper_func
    return try_connection
      
      
@decoTryConnection("iterator")                   
def yolo(arg1, arg2, distantHost):
    print(arg1, arg2,distantHost,  "inside the yolo")
    
if __name__ == '__main__':
    
    
    yolo(34, "tchata")
    # yolo()