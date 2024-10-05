from internal.game_controller import GameController
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from internal.games.player_input import PlayerInput


def to_player_input(ev: dict[str, any]) -> PlayerInput:
  player_input = ev["player_input"]
  action = player_input["action"]
  data = None
  if "data" in player_input:
    data = player_input["data"]
  return PlayerInput(action, data)

class WeboscketGameServer:
  controller: GameController
  def __init__(self, controller: GameController) -> None:
    self.controller = controller
  
  
  async def connect(self, websocket: WebSocket, game_key: str, client_id: str):
    print(websocket.headers)
    print("client key", client_id)
    self.controller.add_player(game_key=game_key, player_id=client_id, ws=websocket)
    await self.controller.broadcast_game_state(game_key=game_key)

    while True:
      event = {}
      
      try:
        event = await websocket.receive_json()
      except Exception as e:
        await self.controller.disconnect_player(player_id=client_id, game_key=game_key)
        break
      
      print("got event", event)
      player_input = to_player_input(event)
      
      game = self.controller.get_game(game_key=game_key)
      if not game is None:
        game.play_game(player_input=player_input)
        await self.controller.broadcast_game_state(game_key=game_key)
          
