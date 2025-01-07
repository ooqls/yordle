from pydantic import BaseModel

GameKey = str
PlayerID = str

class GameStateResponse(BaseModel):
  game_key: GameKey
  game_name: str
  state: dict

class NewGameResponse(BaseModel):
  game_key: GameKey = ""
  
class Game(BaseModel):
    name: str = ""
    display_name: str = ""
    key: str = ""
  
class GameListResponse(BaseModel):
    active_games: list[Game] = list()
    game_list: list[Game] = list()
    
