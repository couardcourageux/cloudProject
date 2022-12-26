




import asyncio


class SignalHandler:
    KEEP_PROCESSING = True
    
    @classmethod
    async def stopGrpcServer(self, time=0):
        await asyncio.sleep(time)
        self.KEEP_PROCESSING = False
        
    @classmethod
    def running(self):
        return self.KEEP_PROCESSING