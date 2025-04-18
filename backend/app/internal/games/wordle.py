from random import randint
import logging
import sys


from datetime import datetime
from internal.records.words import WordDB, get_word_db
from internal.games.player_input import PlayerInput
from internal.games.game_state import State, GameState
from internal.models import GameKey
from internal.games.percent import edit_distance_percent
from internal.games.scores import Score
from internal.games.models import Action, Guess, GuessHistory
from internal.models import PlayerID
from internal.games.wordle_translator import WordleTranslator


logger = logging.getLogger(__name__)

GAME_KEY: str = "yordle"
DISPLAY_NAME: str = "⚔️ Competitve Yordle"
STARTING_DELAY = 5
GAME_TIME = 100


class WordleGameState(GameState):
  def __init__(self, admin: str, key: str, word_db: WordDB):
    self.word_db = word_db
    self.game_key = key
    self.guess_history: dict[str, list[Guess]] = {}
    self.start_time = datetime.now()
    self.admin = admin
    self.game_time = GAME_TIME
    self.current_guess = {id: {} for id in range(50)}
    self.word_index = {}
    self.words = []
    self.state = State.INITIALIZING
    self.scores: dict[str, Score] = {}
    self.translator: WordleTranslator = WordleTranslator()
    
    self.action_mapping = {
      State.WAITING: {
        Action.START: self.start_game,
      },
      State.ACTIVE: {
        Action.ADD: self.add_to_guess,
        Action.BACKSPACE: self.backspace,
        Action.SUBMIT: self.submit_answer
      },
    }
  
  def add_player(self, player_id: PlayerID):
    if player_id not in self.scores:
      self.scores[player_id] = Score()
    if player_id not in self.word_index:
      self.word_index[player_id] = 0
    if player_id not in self.current_guess:
      self.current_guess[0][player_id] = ""
    if player_id not in self.guess_history:
      self.guess_history[player_id] = []
      
  def remove_player(self, player_id: PlayerID):
    if player_id in self.scores:
      del self.scores[player_id]
    if player_id in self.word_index and player_id in self.current_guess[self.word_index[player_id]]:
      del self.current_guess[self.word_index[player_id]][player_id]
    if player_id in self.word_index:
      del self.word_index[player_id]
    if player_id in self.guess_history:
      del self.guess_history[player_id]
    
  def get_players(self) -> set[PlayerID]:
    return set(self.scores.keys())
  
  def get_answer(self, player_id: PlayerID) -> str:
    if player_id not in self.word_index:
      self.add_player(player_id)
    
    return self.words[self.word_index[player_id]]
  
  def get_current_guess(self, player_id: PlayerID) -> str:
    
    if player_id not in self.word_index:
      self.add_player(player_id)
    if player_id not in self.current_guess[self.word_index[player_id]]:
      self.current_guess[self.word_index[player_id]][player_id] = ""
      
    return self.current_guess[self.word_index[player_id]][player_id]
    
  def set_current_guess(self, player_id: PlayerID, guess: str):
    self.current_guess[self.word_index[player_id]][player_id] = guess
    
  def increment_word_index(self, player_id: PlayerID):
    del self.current_guess[self.word_index[player_id]][player_id]
    self.word_index[player_id] = (self.word_index[player_id] + 1) % len(self.words)
    self.current_guess[self.word_index[player_id]][player_id] = ""
  
  def reset_current_guess(self, player_id: PlayerID):
    self.current_guess[self.word_index[player_id]][player_id] = ""
  
  def add_to_guess_history(self, player_id: PlayerID, guess: str, colors: list[str]):
    self.guess_history[player_id].insert(0, Guess(guess=guess, colors=colors))

  def reset_guess_history(self, player_id: PlayerID):
    self.guess_history[player_id] = []
  
  def get_guess_history(self, player_id: PlayerID) -> list:
    if player_id not in self.guess_history:
      self.add_player(player_id)
    return self.guess_history[player_id]

  
  def add_to_guess(self, player_id: str, addition: str):
    current_guess = self.get_current_guess(player_id)
    new_guess = current_guess + addition
    new_guess = new_guess[-len(self.get_answer(player_id=player_id)):]
    self.set_current_guess(player_id, new_guess)
      
  
  def backspace(self, player_id: str, _: any):
    current_guess = self.get_current_guess(player_id)
    if len(current_guess) == 0:
      return
    if len(current_guess) == 1:
      self.set_current_guess(player_id, "")
    else:
      self.set_current_guess(player_id, current_guess[:len(current_guess)-1])

  def start_game(self, player_id: str, _: any):
    if player_id == self.admin:
      self.start_time = datetime.now()
      self.state = State.STARTING

  def submit_answer(self, player_id: str, _: any):
    current_guess = self.get_current_guess(player_id)
    answer = self.get_answer(player_id).upper()
    if len(current_guess) == 0:
      return
    
    self.set_current_guess(player_id, "")
    
    if player_id not in self.scores:
      self.scores[player_id] = Score()
    
    self.scores[player_id].add_score(5)
    
    (guess, colors, is_correct) = self.translator.translate(answer, current_guess)    
    if is_correct:
      self.scores[player_id].add_score(2500)
      self.scores[player_id].add_multiplier(1)
      self.increment_word_index(player_id)
      self.reset_guess_history(player_id)
    else:
      self.add_to_guess_history(player_id=player_id, guess=guess, colors=colors)
      self.scores[player_id].add_multiplier(-0.1)
    
 
  def play_game(self, id: str, player_input: PlayerInput):
    action = player_input.get_action()
    data = player_input.get_data()
    logger.info("action: %s, client id: %s, admin id: %s", action, id, self.admin)
    if self.state in self.action_mapping:
      action_mapping = self.action_mapping[State(self.state)]
      if Action(action) in action_mapping:
        action_func = action_mapping[Action(action)]
        action_func(id, data)
    
    return  
  def update(self):
    if self.state == State.INITIALIZING:
      try:
        self.words = self.word_db.get_random_word_list(100)
      except Exception as e:
        logger.error(e)
        self.state = State.OVER
      self.state = State.WAITING
    elif self.state == State.STARTING:
      time_elapsed = (datetime.now() - self.start_time).total_seconds()
      if time_elapsed > STARTING_DELAY:
        self.start_time = datetime.now()
        self.state = State.ACTIVE  
    elif self.state == State.ACTIVE:
      time_elapsed = (datetime.now() - self.start_time).total_seconds()
      if time_elapsed > self.game_time:
        self.state = State.OVER
        for id, score in self.scores.items():
          score.reset_multiplier()
    
    

  def get_start_time(self) -> datetime:
    return self.start_time

  def get_state(self, player_id: PlayerID) -> dict:
    state = {
      "state": str(self.state),
      "current_guess": self.current_guess[self.word_index[player_id]],
      "guess_history": GuessHistory(guesses=self.get_guess_history(player_id)).model_dump(),
      "scores": {id: score.get_score() for id, score in self.scores.items()},
      "word_index": self.word_index,
      "is_admin": player_id == self.admin,
    }
        
    if self.state in [State.ACTIVE, State.STARTING]:
      time_elapsed = (datetime.now() - self.start_time).total_seconds()
      time_left = GAME_TIME - time_elapsed
      state["time_left"] = time_left
      state["time_elapsed"] = time_elapsed
      state["answer_len"] = {pid: len(self.words[index]) for (pid, index) in self.word_index.items()}
    
    return state

  def get_display_name(self) -> str:
    return DISPLAY_NAME
  
  def get_game_key(self) -> GameKey:
    return self.game_key
  
  def get_game_name(self):
    return GAME_KEY
  
  def game_over(self):
    self.state = State.OVER
      
  def is_over(self) -> bool:
    return str(self.state) == str(State.OVER)
  
    
    
def new_yordle_game(admin_id: str, key: str) -> WordleGameState:
  champ_db = get_word_db()
  if champ_db is None:
    logger.error("please init champ db")
    sys.exit(1)
  return WordleGameState(admin=admin_id, key=key, word_db=champ_db)

      

