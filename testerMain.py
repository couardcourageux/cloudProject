from threadWrapper import ThreadWrapper, killMultiple
import asyncio


def init_network(wrappers, mainWrapper, n):
    mainProc = ThreadWrapper(5005, None)
    mainWrapper = mainProc.id
    wrappers[mainWrapper] = mainProc

    for i in range(1, n+1):
        proc = ThreadWrapper(5005 + i, wrappers[mainWrapper].address())
        wrappers[proc.id] = proc

    wrappers[mainWrapper].run()
    
    for k, w in wrappers.items():
        if k != mainWrapper:
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



async def main():
    wrappers, mainWrapper = init_network({}, "", 2)
            
    await asyncio.sleep(3)
    wrappers, mainWrapper = await terminate_network(wrappers, mainWrapper)
asyncio.run(main())

# clientProc = ThreadWrapper(5006, mainProc.address())
# mainProc.run()
# clientProc.run()


# mainProc = ThreadWrapper(5005, None)
# mainProc.run()

# clientProc = ThreadWrapper(5006, "localhost:5005")
# clientProc.run()