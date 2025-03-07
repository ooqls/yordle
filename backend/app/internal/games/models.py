from enum import Enum
from pydantic import BaseModel
import random

class Action(Enum):
  ADD = "ADD"
  BACKSPACE = "BACKSPACE"
  SUBMIT = "SUBMIT"
  START = "START"

class Guess(BaseModel):
  guess: str = ""
  colors: list[str] = list()
  id: str = ""
  
  def __init__(self, guess: str, colors: list[str]):
    id = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
    super().__init__(guess=guess, colors=colors, id=id)

class GuessHistory(BaseModel):
  guesses: list[Guess] = list()
  
  
  