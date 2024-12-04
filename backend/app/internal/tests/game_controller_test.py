from internal.game_controller import GameController
from internal.games.tests.mock_game_state import MockGameState
from internal.tests.mock_websocket import MockSocket
import internal.records.words as words
import unittest

test_game_key = "mock"

def new_game_controller():
  ctrl = GameController()
  ctrl.game_map[test_game_key] = MockGameState
  return ctrl

def new_mock_websocket():
  return MockSocket()

class TestGameController(unittest.IsolatedAsyncioTestCase):
  async def asyncSetUp(self):
    words.set_word_db("/tmp/test.db")
    return await super().asyncSetUp()
  
  def test_new_game(self):
    ctrl = new_game_controller()
    resp = ctrl.new_game("admin", "wordle", test_game_key)
    self.assertIsNotNone(resp)
    self.assertIsNotNone(resp.game_key)
    self.assertEqual(resp.game_key, test_game_key)
  
  def test_get_game_list(self):
    ctrl = new_game_controller()
    resp = ctrl.get_game_list()
    self.assertIsNotNone(resp)
    self.assertEqual(len(resp), 2)
  
  def test_get_active_games(self):
    ctrl = new_game_controller()
    resp = ctrl.get_active_games()
    self.assertIsNotNone(resp)
    self.assertEqual(len(resp), 0)
    
    ctrl.new_game("admin", "wordle", test_game_key)
    resp = ctrl.get_active_games()
    self.assertIsNotNone(resp)
    self.assertEqual(len(resp), 1)
    
  def test_add_player(self):
    ctrl = new_game_controller()
    ws = new_mock_websocket()
    
    ctrl.new_game("admin", "wordle", test_game_key)
    ctrl.add_player(test_game_key, "player1", ws)
    players = ctrl.get_players_in_game(test_game_key)
    self.assertIsNotNone(players)
    self.assertEqual(len(players), 1)
  
  async def test_remove_player(self):
    ctrl = new_game_controller()
    ws = new_mock_websocket()
    
    ctrl.new_game("admin", "wordle", test_game_key)
    ctrl.add_player(test_game_key, "player1", ws)
    await ctrl.disconnect_player("player1", test_game_key)
    
    players = ctrl.get_players_in_game(test_game_key)
    print(players)
    self.assertIsNotNone(players)
    self.assertEqual(len(players), 0)
    self.assertTrue(ws.closed)
  async def test_broadcast_game_state(self):
    ctrl = new_game_controller()
    ws = new_mock_websocket()
    
    ctrl.new_game("admin", test_game_key, test_game_key)
    ctrl.add_player(test_game_key, "player1", ws)
    await ctrl.broadcast_game_state(test_game_key)
    
    
    self.assertTrue(len(ws.server_messages) > 0)
    game = ctrl.get_game(test_game_key)
    game.over = True
    
    await ctrl.broadcast_game_state(test_game_key)
    self.assertTrue(ws.closed)
    
    

if __name__ == "__main__":
  unittest.main()
  
    
  