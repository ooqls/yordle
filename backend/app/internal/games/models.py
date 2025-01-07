from enum import Enum
from pydantic import BaseModel

class Action(Enum):
  ADD = "ADD"
  BACKSPACE = "BACKSPACE"
  SUBMIT = "SUBMIT"
  START = "START"
  

  
class Guess(BaseModel):
  guess: str = ""
  colors: list[str] = list()

class GuessHistory(BaseModel):
  guesses: list[Guess] = list()
  
  
  