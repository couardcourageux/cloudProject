from grpc import aio
import protocol_pb2
import protocol_pb2_grpc
from kvStoreServicer import KvStoreServicer

import asyncio
import signal




class KeepAlive:
    keepAlive = True
    
    @classmethod
    def exit_gracefully(self):
        KeepAlive.keepAlive = False
        
    @classmethod
    async def checkMustKeepAlive(self, server):
        while KeepAlive.keepAlive:
            await asyncio.sleep(2)
        await server.stop(grace=2)
        
        
class SignalHandler:
    KEEP_PROCESSING = True
    signal.signal(signal.SIGINT, KeepAlive.exit_gracefully)
    signal.signal(signal.SIGTERM, KeepAlive.exit_gracefully)
    
    @classmethod
    async def stopGrpcServer(self, time=0):
        await asyncio.sleep(time)
        KeepAlive.exit_gracefully()

    
async def serving(portToServe:str, server):                                                       
    protocol_pb2_grpc.add_KvStoreServicer_to_server(KvStoreServicer(), server)        
    listen_addr = 'localhost:{}'.format(portToServe)                                                  
    server.add_insecure_port(listen_addr)                                       
    # logging.info("Starting server on %s", listen_addr)   
    print("Starting server on %s", listen_addr)                       
    await server.start()     
    print("server started")                                                   
    await server.wait_for_termination()
    print("server stopped mdr")
    

async def serve(portToServe:str):
    server = aio.server()
    await asyncio.gather(serving(portToServe, server), KeepAlive.checkMustKeepAlive(server))
    