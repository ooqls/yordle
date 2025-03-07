from functools import lru_cache
import random
_possible_colors: list[str] = [
  "Red", "Green", "Yellow", "Cyan", "Magenta", "Orange", "Purple", "Brown", "Pink"
]

def _get_random_color() -> str:
    return random.choice(_possible_colors)

@lru_cache
def _build_letter_count(word: str) -> dict[str, int]:
  letter_count = dict()
  for c in word:
    if not c in letter_count:
      letter_count[c] = 0
    letter_count[c] += 1
  return letter_count

class WordleTranslator:
  def __init__(self, ):
    self.right_place_right_letter = _get_random_color()
    self.wrong_place_right_letter = _get_random_color()
    self.wrong_place_wrong_letter = _get_random_color()
  
  def translate(self, answer: str, guess: str) -> tuple[str, list[str], bool]:
    is_correct = True
    output = ""
    
    player_input = guess.upper() + ("_" * max((len(answer) - len(guess), 0)))
    self._modify_symbols()
      
    
    m_len = min(len(answer), len(player_input))
    output = ["" for _ in range(m_len) ]
    letter_count = _build_letter_count(answer)
    
    
    for i in range(m_len):
      color = ""
      
      if player_input[i] not in letter_count:
        letter_count[player_input[i]] = 0
      letter_count[player_input[i]] += 1
      
      if player_input[i] == answer[i]:
        color = self.right_place_right_letter
      else:
        is_correct = False
        if player_input[i] in answer:
          color = self.wrong_place_right_letter
        else:
          color = self.wrong_place_wrong_letter
      
      output[i] = color
    
    for letter in letter_count:
      if letter in letter_count:
        if letter_count[letter] != letter_count[letter]:
          is_correct = False
          break
      else:
        is_correct = False
        break
    
    return guess, output, is_correct
      
  def _modify_symbols(self):
    self.right_place_right_letter = _get_random_color()
    self.wrong_place_right_letter = _get_random_color()
    self.wrong_place_wrong_letter = _get_random_color()