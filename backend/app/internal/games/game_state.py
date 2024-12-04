from internal.games.player_input import PlayerInput
from internal.models import GameKey, PlayerID
from enum import Enum


class State(Enum):
  INITIALIZING = 0
  STARTING = 1
  ACTIVE = 2
  OVER = 3
  WAITING = 4


class GameState:
  def get_game_key(self) -> GameKey:
    pass
  def get_game_name(self) -> str:
    pass
  def play_game(self, id: str, player_input: PlayerInput):
    pass
  def get_state(self, player_id: PlayerID) -> dict:
    pass
  def add_player(id: PlayerID):
    pass
  def update(self):
    pass
  def is_over(self):
    pass
  def get_start_time(self):
    pass
  def get_players() -> set[PlayerID]:
    pass
