from fastapi.websockets import WebSocket as FastWebSocket, WebSocketState
import logging

logger = logging.getLogger(__name__)
class Socket:
  
  async def send(self, ev: dict[str, any]):
    pass
  
  async def recieve(self) -> dict[str, any]:
    pass
  
  async def close(self, code: int = 1000, reason: str = ''):
    pass
    
class WebSocket(Socket):
  _ws: FastWebSocket
  
  def __init__(self, ws: FastWebSocket) -> None:
    self._ws = ws
    
  async def send(self, ev: dict[str, any]):
    await self._ws.send_json(ev)
    
  
  async def recieve(self) -> dict[str, any]:
    return await self._ws.receive_json()
    
  
  async def close(self, code: int = 1000, reason: str = ''):
    logger.info("closing websocket: %s", self._ws.client_state)
    if self._ws is not None and self._ws.client_state == WebSocketState.CONNECTED:
      await self._ws.close(code, reason)
