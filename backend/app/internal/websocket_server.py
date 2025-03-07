from internal.game_controller import GameController
from fastapi import FastAPI, WebSocketDisconnect
from internal.websocket import Socket
from internal.games.player_input import PlayerInput
import asyncio

import logging

logger = logging.getLogger(__name__)


def to_player_input(ev: dict[str, any]) -> PlayerInput:
  player_input = ev["player_input"]
  action = player_input["action"]
  data = None
  if "data" in player_input:
    data = player_input["data"]
  return PlayerInput(action, data)

class WeboscketGameServer:
  controller: GameController
  broadcast_task: asyncio.Task
  
  def __init__(self, controller: GameController) -> None:
    self.controller = controller
    self.broadcast_task = asyncio.create_task(self.start_broadcasting())
    
  
  async def start_broadcasting(self):
    while True:
      for game in self.controller.get_active_games():
        try:
          await self.controller.broadcast_game_state(game_key=game.key)
          await self.controller.update_state(game.key)
        except Exception as e:
          logger.error("error %s", e)
      await asyncio.sleep(1)
  
  def get_controller(self) -> GameController:
    return self.controller
  
  async def disconnect_player(self, websocket: Socket, game_key: str, client_id: str):
    await self.controller.disconnect_player(player_id=client_id, game_key=game_key)
    await websocket.close()  
  
  async def connect(self, websocket: Socket, game_key: str, game_type: str, client_id: str):
    try:
      await self._connect(websocket, game_key, game_type, client_id)
    except WebSocketDisconnect as e:
      if e.reason != "game_over":
        logger.error("websocket disconnect reason %s", e.reason)
    except Exception as e:
      logger.error("error %s", e)
      await self.disconnect_player(websocket, game_key, client_id)
    
  async def _connect(self, websocket: Socket, game_key: str, game_type: str, client_id: str):
    
    if self.controller.get_game(game_key=game_key) is None:
      self.controller.new_game(player_id=client_id, game_type=game_type, key=game_key)
    
    self.controller.add_player(game_key=game_key, player_id=client_id, ws=websocket)
    await self.controller.broadcast_game_state(game_key=game_key)

    while True:      
      event = await websocket.recieve()
  
      
      player_input = to_player_input(event)
      game = self.controller.get_game(game_key=game_key)
      if not game is None:
        game.play_game(id=client_id, player_input=player_input)
        await self.controller.broadcast_game_state(game_key=game_key)

