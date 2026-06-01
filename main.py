from fastapi import FastAPI
from routers import players, game_items, purchases

app = FastAPI(title="게임 아이템 상점")

app.include_router(players.router)
app.include_router(game_items.router)
app.include_router(purchases.router)
