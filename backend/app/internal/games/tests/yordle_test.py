import unittest
import asyncio

from internal.games.wordle import WordleGameState
from internal.records.test.mock_word_db import new_test_word_db
from internal.games.player_input import PlayerInput
from internal.games.wordle import Action, State

admin = "admin"

def new_wordle_game():
  db = new_test_word_db()
  return WordleGameState(admin="admin",key="test", word_db=db)

class YordleTestCase(unittest.IsolatedAsyncioTestCase):
  async def test_starting_delay(self):
    y = new_wordle_game()
    y.game_time = 10
    
    y.update()
    
    self.assertEqual(y.get_state("")["state"], str(State.WAITING))
    y.play_game(admin, player_input=PlayerInput(action=Action.START, data=""))
    self.assertEqual(y.get_state("")["state"], str(State.STARTING))
    state_changed = False
    for i in range(10):
      y.update()
      if y.get_state("")["state"] == str(State.ACTIVE):
        state_changed = True
        break
      await asyncio.sleep(1)
      
    self.assertTrue(state_changed)
    
    for i in range (10):
      y.update()
      if y.get_state("")["state"] == str(State.OVER):
        break
      await asyncio.sleep(1)
    
    y.update()
    self.assertTrue(y.is_over())
    self.assertEqual(y.get_state("")["state"], str(State.OVER))

if __name__ == "__main__":
  unittest.main()
    