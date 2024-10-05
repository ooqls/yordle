from random import randint
import random
import string
from datetime import datetime
from internal.records.champs import ChampDB, get_champ_db
from internal.games.player_input import PlayerInput
from internal.games.game_state import State, GameState
from internal.models import GameKey
from internal.games.game_key import generate_game_key
from internal.games.percent import edit_distance_percent
from enum import Enum


import os

import sys

_possible_symbols: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+{}|:<>?[];',./"
GAME_NAME: str = "yordle"

class Action(Enum):
  ADD = "ADD"
  BACKSPACE = "BACKSPACE"
  SUBMIT = "SUBMIT"


class YordleGameState(GameState):
  heros: list[str] = list()
  answer: str = ""
  current_guess: str = ""
  guess_history: list[(str, str)] = []
  letter_count: dict[str, int] = dict()
  state: State = State.ACTIVE
  game_key: GameKey = ""
  
  right_place_right_letter: str = ""
  wrong_place_right_letter: str = ""
  wrong_place_wrong_letter: str = ""
  
  def get_answer(self) -> str:
    return self.answer
  
  def __init__(self, answer: str, champ_db: ChampDB):
    self.answer = answer
    self.champ_db = champ_db
    self.game_key = generate_game_key()
    self.action_mapping = {
      State.ACTIVE: {
        Action.ADD: self.add_to_guess,
        Action.BACKSPACE: self.backspace,
      },
    }
    
    for c in self.answer:
      if not c in self.letter_count:
        self.letter_count[c] = 0
      self.letter_count[c] += 1
  
  def _get_random_symbol(self) -> str:
    n = randint(0, len(_possible_symbols))
    n2 = randint(1, 3) + n % len(_possible_symbols)
    return _possible_symbols[n:n2]
  
  def _modify_game(self):
    self.right_place_right_letter: str = self._get_random_symbol()
    self.wrong_place_right_letter: str = self._get_random_symbol()
    self.wrong_place_wrong_letter: str = self._get_random_symbol()
    print(f"right place right letter: {self.right_place_right_letter}")
  
  def add_to_guess(self, addition: str):
    new_guess = self.current_guess + addition
    new_guess = new_guess[-len(self.answer):]
    self.current_guess = new_guess
    
    if self.current_guess == self.answer:
      self.state = State.WON
      
  
  def backspace(self, _: any):
    if len(self.current_guess) == 0:
      return
    if len(self.current_guess) == 1:
      self.current_guess = ""
    else:
      self.current_guess = self.current_guess[:len(self.current_guess)-1]

  # def submit_answer(self):
  #   is_correct = True
  #   output = list()
  #   player_input = self.answer
  #   self._modify_game()
    
  #   m_len = min(len(self.answer), len(player_input))
  #   output = [self.wrong_place_wrong_letter for _ in range(m_len)]
  #   letter_count = self.letter_count.copy()
    
  #   for i in range(m_len):
  #     letter = ''
      
  #     if player_input[i] == self.answer[i]:
  #       letter = self.right_place_right_letter
  #     else:
  #       is_correct = False
        
  #       if player_input[i] in self.answer and letter_count[player_input[i]] > 0:
  #         letter = self.wrong_place_right_letter
  #       else:
  #         letter = self.wrong_place_wrong_letter
      
  #     if self.answer[i] in letter_count:
  #       letter_count[self.answer[i]] -= 1
      
  #     output.append(letter)

  #     message = " | ".join([*player_input])
  #     message += "\n"
  #     message += " | ".join([*output])
      
  #   if is_correct:
  #     self.state = State.WON
        
  def play_game(self, player_input: PlayerInput):
    action = player_input.get_action()
    data = player_input.get_data()
    if self.state in self.action_mapping:
      action_mapping = self.action_mapping[State(self.state)]
      action_func = action_mapping[Action(action)]
      action_func(data)
    
    return 
  def get_state(self):
    return {"state": str(self.state), "answer_len": len(self.answer), "current_guess": self.current_guess, "correct_percent": edit_distance_percent(answer=self.answer, guess=self.current_guess)}

  def get_game_name(self) -> str:
    return GAME_NAME
  
  def get_game_key(self) -> GameKey:
    return self.game_key
    

def new_yordle_game() -> YordleGameState:
  champ_db = get_champ_db()
  if champ_db is None:
    print("please init champ db")
    sys.exit(1)
    
  return YordleGameState(champ_db.get_todays_champion(), champ_db)

      

