# /usr/bin/python3

import yordle
from game import run_game
import os


def main():
  t = input("Which game type: (1 todays hero, 2 random, 3 use env var)")
  if t == "1":
    run_game(yordle.get_todays_hero())
  elif t == "2":
    run_game(yordle.get_random_hero())
  else:
    run_game(os.environ["YORDLE_ANSWER"])

if __name__ == "__main__":
  main()