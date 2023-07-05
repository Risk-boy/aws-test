from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.games import Games
from app.get_games import GetGames


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "LOL"},
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    input = q
    # print(keyword)
    tier, division = input.split()
    # print(tier, division)
    get_lol = GetGames()
    games = await get_lol.search(tier, division, 1)
    print(games)
    game_lists = []
    for game in games:
        game_model = Games(
            tier=tier,
            division=division,
            leagueId=game["leagueId"],
            summonerId=game["summonerId"],
            summonerName=game["summonerName"],
        )
        game_lists.append(game_model)
        # print(game_model)
    # print(game_lists)
    await mongodb.engine.save_all(game_lists)
    print(game_lists)

    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "LoL", "games":games, "division":division},
    )


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
