from grpc import aio
import protocol_pb2
import protocol_pb2_grpc
from kvStoreServicer import KvStoreServicer

async def serve(portToServe:str):
    server = aio.server()                                                       
    protocol_pb2_grpc.add_KvStoreServicer_to_server(KvStoreServicer(), server)        
    listen_addr = 'localhost:{}'.format(portToServe)                                                  
    server.add_insecure_port(listen_addr)                                       
    # logging.info("Starting server on %s", listen_addr)   
    print("Starting server on %s", listen_addr)                       
    await server.start()     
    print("server started")                                                   
    await server.wait_for_termination()