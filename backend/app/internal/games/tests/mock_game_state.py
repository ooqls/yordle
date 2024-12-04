from internal.games.game_state import GameState
from internal.games.player_input import PlayerInput
from internal.models import GameKey, PlayerID
from datetime import datetime


class MockGameState(GameState):
  players = []
  over: bool = False
  start_time: datetime = datetime.now()
  admin_id: str = ""
  game_key: str = "mock"
  
  def __init__(self, admin_id: str, game_key: GameKey = "mock"):
    self.admin_id = admin_id
    self.game_key = game_key
  
  def get_game_key(self) -> GameKey:
    return "mock"
  def get_game_name(self) -> str:
    return "mock"
  def play_game(self, id: str, player_input: PlayerInput):
    return
  def get_state(self, player_id: PlayerID) -> dict:
    return {"state": "mock"}
  def add_player(self, id: str):
    self.players.append(id)
  def update(self):
    return
  def is_over(self) -> bool:
    return self.over
  def get_start_time(self):
    return self.start_time