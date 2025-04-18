# generated by fastapi-codegen:
#   filename:  openapi.yaml
#   timestamp: 2024-07-31T21:12:20+00:00

from __future__ import annotations

from fastapi import FastAPI, Cookie
from fastapi.websockets import WebSocket as FastWebSocket
from internal.game_controller import GameController, NewGameResponse
from internal.websocket_server import WeboscketGameServer
from internal.websocket import WebSocket
from internal.records.words import init_word_db
from internal.models import NewGameResponse, GameStateResponse, GameListResponse
from asyncio import create_task
from typing import Annotated
from fastapi import FastAPI, Header, HTTPException
import random
from english_words import get_english_words_set

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



api: FastAPI = FastAPI(
    title='yordle',
    version='1.0.0',
    servers=[{'url': '/'}],
    
)


init_word_db()

words = get_english_words_set(['web2'], lower=2)


def generate_game_key() -> str:
  return random.choice(list(words))

controller = GameController()
server = WeboscketGameServer(controller)
broadcast_task = create_task(server.start_broadcasting())

@api.get(
    '/api/games',
    response_model=GameListResponse,
    responses={'500': {'model': str}},
)
def get_games() -> list[str]:
    """
    get a list of games
    """
    resp = GameListResponse(active_games=controller.get_active_games(), game_list=controller.get_game_list())
    return resp



@api.post(
    '/api/games/{}',
    response_model=NewGameResponse,
    responses={'500': {'model': str}},
)
def start_new_game(game: str, clientid: Annotated[str | None, Header()]) -> str:
    return controller.new_game(clientid, game)

@api.get(
    '/api/{game}/{game_key}',
    response_model=GameStateResponse,
    responses={'200': {'model': dict}, '500': {'model': str}},
)
async def get_game(game: str, game_key: str, clientId: Annotated[str | None, Header()]) -> dict:
    game = controller.get_game(game_key)
    if game is None:
        logger.error("game not found: %s", game_key)
        raise HTTPException(status_code=404, detail="game not found")
    
    return GameStateResponse(game_key=game_key, state=game.get_state(player_id=clientId), game_name=game.get_game_name())

@api.post(
    '/api/{game}/{game_key}',
    response_model=NewGameResponse,
    responses={'500': {'model': str}},
)
def new_game_with_key(game: str, game_key: str, clientid: Annotated[str | None, Header()]) -> str:
    return controller.new_game(clientid, game, game_key)

@api.post(
    '/api/{game}',
    response_model=NewGameResponse,
    responses={'500': {'model': str}},
)
def new_game(game: str, clientid: Annotated[str | None, Header()]) -> str:
    return controller.new_game(clientid, game, generate_game_key())


@api.websocket(
    path='/websocket/{game}/{game_key}/ws',
    name="websocket_endpoint",
)
async def websocket_endpoint(websocket: FastWebSocket, game: str, game_key: str, client_id: str):
    logger.debug("got a websocket", {"game": game, "game_key": game_key, "client_id": client_id})    
    if game_key == "":
        game_key = generate_game_key()
        
    game = controller.get_game(game_key=game_key)
    if game is not None and game.is_over():
        logger.debug("game is over")
        await websocket.close(reason="game_over")
    else:
        print("accepting websocket")
        await websocket.accept()
        websocket.send_json
        await server.connect(WebSocket(websocket), game_key=game_key, game_type=game, client_id=client_id)

@api.post(
    '/error',
    response_model=None,
)
def post_error(error: str) -> str:
    print(error)
    return 
    

# @app.post(
#     '/yordle/{id}/today',
#     response_model=str,
#     responses={'400': {'model': str}, '500': {'model': str}},
# )
# def post_answer(id: str, answer: str = ...) -> str:
#     """
#     post an answer to todays yordle
#     """
    
