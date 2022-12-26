from threadWrapper import ThreadWrapper, killMultiple,mapNetwork,validateNetwork
import asyncio
import json


import os, sys

LOCAL_DIRECTORY = os.getcwd()

sys.path.append(os.path.join(LOCAL_DIRECTORY, "grpc"))

def printListe(liste, title):
    print(f"---------------------------\n{title}\n")
    for el in liste:
        print(el)
        print("\n")
    
        

async def init_network(wrappers, mainWrapper, n):
    mainProc = ThreadWrapper(5005, None)
    mainWrapper = mainProc.id
    wrappers[mainWrapper] = mainProc

    for i in range(1, n+1):
        proc = ThreadWrapper(5005 + i, wrappers[mainWrapper].address())
        wrappers[proc.id] = proc

    wrappers[mainWrapper].run()
    
    for k, w in wrappers.items():
        if k != mainWrapper:
            await asyncio.sleep(1)
            w.run()
            
    return wrappers, mainWrapper


async def terminate_network(wrappers, mainWrapper):
    toKill = []
    for k, w in wrappers.items():
        if k != mainWrapper:
            toKill.append(w)
    await killMultiple(toKill)
    await wrappers[mainWrapper].stop()
    return wrappers, mainWrapper


async def map_network(wrappers, mainWrapper):
    network = await mapNetwork(wrappers, mainWrapper)
    # print(network)
    # net, errs = validateNetwork(network)
    # printListe(net, "network")
    # printListe(errs, "errors")
    # print("---------------------------\n")
    print(json.dumps(network, indent=4))
    



async def main():
    wrappers, mainWrapper = await init_network({}, "", 2)
    
    await asyncio.sleep(5) # delai pour que le réseau soit bien lancé
    print('mapping')
    await map_network(wrappers, mainWrapper)
    print('mapped')

    wrappers, mainWrapper = await terminate_network(wrappers, mainWrapper)
asyncio.run(main())





