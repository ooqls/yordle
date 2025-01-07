import unittest
import internal.websocket_server as ws
import asyncio
from internal.game_controller import GameController
from internal.tests.mock_websocket import MockSocket
import internal.records.words as words
import logging

test_game_type = "yordle"

def new_websocket_server():
  words.set_word_db("/tmp/test.db")
  return ws.WeboscketGameServer(GameController())

class TestGameController(unittest.IsolatedAsyncioTestCase):
  async def test_connect(self):
    server = new_websocket_server()
    ws1 = MockSocket()
    ws2 = MockSocket()
    
    done1 = asyncio.Task(server.connect(websocket=ws1, game_key="mock", game_type=test_game_type, client_id="player1"))
    done2 = asyncio.Task(server.connect(websocket=ws2, game_key="mock", game_type=test_game_type, client_id="player2"))
    await asyncio.sleep(1)
    
    game = server.controller.get_game("mock")

    self.assertIsNotNone(server.get_controller().get_game("mock"))
    self.assertTrue("player1" in server.get_controller().get_game("mock").get_players())

    
    
    await ws1.close()
    try:
      await asyncio.wait_for(done1, timeout=2)
    except Exception as e:
      self.fail("failed to stop the connectiong thread for player1")
    

    game = server.controller.get_game("mock")
    
    self.assertFalse("player1" in game.get_players())
    
    await ws2.close()
    try:
      await asyncio.wait_for(done2, timeout=2)
    except Exception as e:
      self.fail("failed to stop the connectiong thread for player2")
    
    done2.cancel()
    game = server.controller.get_game("mock")
    self.assertIsNone(game)
    
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()