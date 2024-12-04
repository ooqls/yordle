from typing import Callable
import json
from internal.games.game_state import GameState
from internal.models import GameKey, PlayerID, NewGameResponse, Game
from internal.websocket import Socket
import internal.games.wordle as wordle
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)


# 1. broadcast game state to all players
# 2. add current guess to yordle game state

NewGameCallable = Callable[[str, str], GameState]

class NoSuchGameException(Exception):
  pass

class GameController:
  game_map: dict[str, NewGameCallable] = {
    wordle.GAME_NAME: wordle.new_yordle_game
  }
  
  
  def __init__(self):
    self.active_games = dict()
    self.finished_games = dict()
    self.connections = dict()
    self.player_game_mapping = dict()
    

  def get_game_list(self) -> list[str]:
    return [game for game in self.game_map.keys()]
  
  def get_active_games(self) -> list[Game]:
    game_list = list()
    
    for key, game in self.active_games.items():
      if not game.is_over():
        game_list.append(Game(name=game.get_game_name(), key=key))
    
    return game_list
  
  def add_player(self, game_key: GameKey, player_id: PlayerID, ws: Socket):
    if not game_key in self.connections:
      self.connections[game_key] = {player_id: ws}
    else:
      if not player_id in self.connections[game_key]:
        self.connections[game_key][player_id] = ws
    
    if not player_id in self.player_game_mapping:
      self.player_game_mapping[player_id] = set([game_key])
    else:
      self.player_game_mapping[player_id].add(game_key)
    
    if game_key in self.active_games:
      self.active_games[game_key].add_player(player_id)

  def remove_game(self, game_key: GameKey):
      if game_key in self.active_games:
        del self.active_games[game_key]
        
        
  async def remove_player_from_game(self, game_key: str, player_id: PlayerID, reason: str = "player_disconnected"):
    if game_key in self.connections:
      player_conns = self.connections[game_key]
      # closes this player's connection to this game
      if player_id in player_conns:
        logger.info("closing player connection %s, reason: %s", player_id, reason)
        ws = player_conns[player_id]
        await ws.close(reason=reason)
        del player_conns[player_id]
        
      if len(player_conns) == 0:
        self.remove_game(game_key)
      
    if game_key in self.active_games:
      game = self.active_games[game_key]
      game.remove_player(player_id) 
        
  async def disconnect_player(self, player_id: PlayerID, game_key: GameKey = None, reason: str = "player_disconnected"):
    logger.info("disconnecting %s", player_id)
    if player_id in self.player_game_mapping:
      games = self.player_game_mapping[player_id]
      if game_key is not None and game_key in games:
        await self.remove_player_from_game(game_key, player_id, reason=reason)
    
    # closes  all connections for this player
    # for _, player_cons in self.connections.items():
    #   if player_id in player_cons:
    #     logger.info("closing player connection %s", player_id)
    #     await player_cons[player_id].close(reason=reason)
    #     del player_cons[player_id]
        
      
  def get_game(self, game_key: GameKey) -> GameState:
    if game_key in self.active_games:
      return self.active_games[game_key]
  
    if game_key in self.finished_games:
      return self.finished_games[game_key]
    
    
    
    return None
  
  def get_players_in_game(self, game_key: GameKey) -> dict[PlayerID, Socket]:
    if game_key in self.connections:
      player_conns = self.connections[game_key]
      return player_conns
  
    return dict()
    
  async def update_state(self, game_key):
    if game_key in self.active_games:
      logger.info("updating game state %s", game_key)
      game = self.active_games[game_key]
      game.update()
      
      if game.is_over():
        for player_id in game.get_players():
          logger.info("game over, disconnecting player")
          await self.disconnect_player(player_id=player_id, game_key=game_key, reason="game_over")
        self.finished_games[game_key] = game
        self.remove_game(game_key)
      
      
  async def broadcast_game_state(self, game_key: str):
    logger.info("gamekey: %s", game_key)
    if game_key in self.active_games and game_key in self.connections:
      game = self.active_games[game_key]
      player_conns = self.get_players_in_game(game_key).copy()
      
      if len(player_conns) == 0:
        self.remove_game(game_key)
        return
      
      logger.debug("cons %s", player_conns)
      for player_id, conn in player_conns.items():
        logger.info("sending to player %s", player_id)
        ev = {"event": "game_update", "game_Key": game_key, "state": game.get_state(player_id)}
        
        try:
          await conn.send(ev)
        except Exception as e:
          logger.error("error sending to player %s: %s", player_id, e)
          await self.disconnect_player(player_id, game_key, reason="error_sending")
      
          
  
  def new_game(self, player_id: str, game_type: str, key: str) -> NewGameResponse:
    if game_type not in self.game_map:
      raise NoSuchGameException(game_type + " not found")
    game_state = self.get_game(game_key=key)
    if game_state is None:
      game_state = self.game_map[game_type](player_id, key)
      self.active_games[game_state.get_game_key()] = game_state
      
    return NewGameResponse(game_key=game_state.get_game_key())
    
    

