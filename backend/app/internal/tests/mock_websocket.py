import asyncio

class ClosedException(Exception):
    def __init__(self):
        super().__init__("Socket is closed")

class MockSocket:
    def __init__(self):
        self.server_messages = []
        self.client_messages = []
        self.closed = False

    async  def send(self, message):
        if self.closed:
            raise ClosedException()
        
        self.server_messages.append(message)
    
    def send_as_client(self, message):
        if self.closed:
            raise ClosedException()
        
        self.client_messages.append(message)

    async def recieve(self):
        while len(self.client_messages) == 0:
            await asyncio.sleep(0.1)
            if self.closed:
                raise ClosedException()
        
        return self.client_messages.pop(0)

    async def close(self, code=1000, reason=""):
        self.closed = True
        return