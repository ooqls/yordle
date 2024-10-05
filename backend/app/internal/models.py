from pydantic import BaseModel

GameKey = str
PlayerId = str

class NewGameResponse(BaseModel):
  game_key: GameKey = ""