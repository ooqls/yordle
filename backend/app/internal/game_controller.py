from typing import Callable
from fastapi.websockets import WebSocket
import websockets.server
import json
from internal.games.game_state import GameState
from internal.models import GameKey, PlayerId, NewGameResponse
import internal.games.yordle as yordle


# 1. broadcast game state to all players
# 2. add current guess to yordle game state

NewGameCallable = Callable[[], GameState]


class GameController:
  active_games: dict[GameKey, GameState] = dict()
  connections: dict[GameKey, dict[PlayerId, websockets.WebSocketServerProtocol]] = dict()
  player_game_mapping: dict[PlayerId, set[GameKey]] = dict()
  game_map: dict[str, NewGameCallable] = {
    yordle.GAME_NAME: yordle.new_yordle_game
  }
  
  def get_game_list(self) -> list[str]:
    return [game for game in self.game_map.keys()]
  
  def get_active_games(self) -> list[any]:
    game_list = list()
    for key, game in self.active_games.items():
      game_list.append({"key": key, "name": game.get_game_name()})
    
    return game_list
  
  def add_player(self, game_key: GameKey, player_id: PlayerId, ws: WebSocket):
    if not game_key in self.connections:
      self.connections[game_key] = {player_id: ws}
    else:
      if not player_id in self.connections[game_key]:
        self.connections[game_key][player_id] = ws
    
    if not player_id in self.player_game_mapping:
      self.player_game_mapping[player_id] = set([game_key])
    else:
      self.player_game_mapping[player_id].add(game_key)

  def remove_game(self, game_key: GameKey):
    if game_key in self.active_games:
      del self.active_games[game_key]
    
  async def remove_player_from_game(self, game_key: str, player_id: PlayerId):
    if game_key in self.connections:
      player_conns = self.connections[game_key]
      if player_id in player_conns:
        ws = player_conns[player_id]
        if ws.state == websockets.server.State.OPEN:
          await ws.close()
        del player_conns[player_id]
        
      if len(player_conns) == 0:
        self.remove_game(game_key)
        
  async def disconnect_player(self, player_id: PlayerId, game_key: GameKey = None):
    print("disconnecting ", player_id)
    if player_id in self.player_game_mapping:
      games = self.player_game_mapping[player_id]
      
      if game_key is not None and game_key in games:
        await self.remove_player_from_game(game_key, player_id)
        
      
  def get_game(self, game_key: GameKey) -> GameState:
    if game_key in self.active_games:
      return self.active_games[game_key]
    
    return None
  
  def get_players_in_game(self, game_key: GameKey) -> dict[PlayerId, WebSocket]:
    if game_key in self.connections:
      player_conns = self.connections[game_key]
      return player_conns
    
    return dict()
    
  async def broadcast_game_state(self, game_key: str):
    print("looking up game key", game_key)
    print(self.active_games, self.connections)
    if game_key in self.active_games and game_key in self.connections:
      game = self.active_games[game_key]
      player_conns = self.get_players_in_game(game_key)
      
      print("number of players in game", len(player_conns))
      for player_id, conn in player_conns.items():
        ev = {"event": "game_update", "state": game.get_state()}
        print(json.dumps(ev))
        try:
          await conn.send_json(ev)
        except Exception as e:
          print("error sending to player", player_id)
          self.disconnect_player(player_id)
  
  def new_game(self, game: str) -> NewGameResponse:
    if game not in self.game_map:
      return None
    
    game_state = self.game_map[game]()
    self.active_games[game_state.get_game_key()] = game_state
    return NewGameResponse(game_key=game_state.get_game_key())
    
    

