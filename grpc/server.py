from grpc import aio
import protocol_pb2
import protocol_pb2_grpc
from kvStoreServicer import KvStoreServicer

import asyncio
from signalHandler import SignalHandler




class KeepAlive:
    keepAlive = True
    
    # @classmethod
    # def exit_gracefully(self):
    #     KeepAlive.keepAlive = False
        
    @classmethod
    async def checkMustKeepAlive(self, server):
        while SignalHandler.KEEP_PROCESSING:
            await asyncio.sleep(2)
        await server.stop(grace=2)
        
        


    
async def serving(portToServe:str, server):                                                       
    protocol_pb2_grpc.add_KvStoreServicer_to_server(KvStoreServicer(), server)        
    listen_addr = 'localhost:{}'.format(portToServe)                                                  
    server.add_insecure_port(listen_addr)                                       
    # logging.info("Starting server on %s", listen_addr)   
    print("Starting server on ", listen_addr)                       
    await server.start()                                                       
    await server.wait_for_termination()
    print("server stopped on ", listen_addr)
    

async def serve(portToServe:str):
    server = aio.server()
    await asyncio.gather(serving(portToServe, server), KeepAlive.checkMustKeepAlive(server))
    