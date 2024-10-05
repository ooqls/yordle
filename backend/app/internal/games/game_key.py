from english_words import get_english_words_set
import random

words = get_english_words_set(['web2'], lower=2)

def generate_game_key() -> str:
  return random.choice(list(words))