import os
import sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "grpc"))

from server import serve
import asyncio

if __name__ == "__main__":
    
    asyncio.run(serve(5000))
    