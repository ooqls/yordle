from internal.records.words import WordDB, get_word_db
from internal.games.game_state import State, GameState
from internal.games.player_input import PlayerInput
from internal.models import GameKey, PlayerID
from internal.games.models  import Action, Guess, GuessHistory
from internal.games.wordle_translator import WordleTranslator
import logging

logger = logging.getLogger(__name__)
GAME_KEY: str = "classicyordle"
DISPLAY_NAME: str = "🪨 Yordle"

def new_classic_wordle_game(id: PlayerID, key: str) -> GameState:
  return ClassicWordleGameState(admin_id=id, key=key)

class ClassicWordleGameState(GameState):
  def __init__(self, admin_id: PlayerID, key: str):
    self.admin_id: PlayerID = admin_id
    self.translator: WordleTranslator = WordleTranslator()
    self.word_db: WordDB = get_word_db()
    self.answer: str = self.word_db.get_random_word()
    self.current_guess: str = ""
    self.answer_len: int = len(self.answer)
    self.state: State = State.ACTIVE
    self.key: GameKey = key
    self.players: set[PlayerID] = set()
    self.guess_history: list[Guess] = list()
    self.is_won: bool = False
    self.max_guesses: int = 5
    self.action_mapping: dict[State, dict[Action, callable]] = {
      State.ACTIVE: {
        Action.ADD: self.add_guess,
        Action.BACKSPACE: self.backspace,
        Action.SUBMIT: self.submit_guess
      }
    }

  def get_game_key(self) -> str:
    """Gets the key for this specific instance of the game

    Returns:
        str: key of this instance of the game
    """
    return self.key
  
  def get_game_name(self) -> str:
    """Gets the name of the actual game

    Returns:
        str: The name of the game
    """
    return GAME_KEY
  
  def get_display_name(self) -> str:
    """Gets the display name of the game
    
    Returns:
        str: The display name of the game
    """
    return DISPLAY_NAME
  
  def add_player(self, id: PlayerID):
    self.players.add(id)
  
  def get_state(self, _: PlayerID):
    return {
      "state": str(self.state),
      "current_guess": self.current_guess,
      "answer_len": len(self.answer),
      "players": list(self.players),
      "guess_history": GuessHistory(guesses=self.guess_history).model_dump(),
      "guesses_left": self.max_guesses - len(self.guess_history),
      "is_won": self.is_won,
    }
  
  def update(self):
    pass
  
  def is_over(self):
    return self.state == State.OVER
  
  def get_start_time(self):
    pass
  
  def get_players(self):
    return self.players
  
  def add_guess(self, id: str, data: str):
    new_guess = self.current_guess + data
    new_guess = new_guess[-len(self.answer):]
    self.current_guess = new_guess
  
  def backspace(self, id: str, data: str):
    self.current_guess = self.current_guess[:-1]
    
  def submit_guess(self, id: str, data: str):
    (guess, colors, correct) = self.translator.translate(self.answer, self.current_guess)
    self.current_guess = ""
    self.guess_history.insert(0, Guess(guess=guess, colors=colors))
    
    if correct:
      self.is_won = True
      self.state = State.OVER
    else:
      self.current_guess = ""
      if len(self.guess_history) >= self.max_guesses:
        self.state = State.OVER
    
  def play_game(self, id: str, player_input: PlayerInput):
    action = player_input.get_action()
    data = player_input.get_data()
    logger.info("action: %s, client id: %s, admin id: %s", action, id, self.admin_id)
    if self.state in self.action_mapping:
      action_mapping = self.action_mapping[State(self.state)]
      if Action(action) in action_mapping:
        action_func = action_mapping[Action(action)]
        action_func(id, data)

  
    