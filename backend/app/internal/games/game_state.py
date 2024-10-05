from internal.games.player_input import PlayerInput
from internal.models import GameKey
from enum import Enum



class State(Enum):
  ACTIVE = 1
  LOST = 2
  WON = 3


class GameState:
  def get_game_key(self) -> GameKey:
    pass
  def get_game_name(self) -> str:
    pass
  def play_game(self, player_input: PlayerInput):
    pass
  def get_state(self) -> dict:
    pass

