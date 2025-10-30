import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from hero_lib.database import init_db
from controller.hero import router as heroes_router
from controller.team import router as teams_router

app = FastAPI(
    title="API de Heróis e Times",
    version="1.1.0",
    contact={
        "name": "Gustavo Saraiva",
        "url": "https://github.com/saraivagustavo",
        "email": "gsaraivam10@gmail.com",
    }
)

init_db()

app.include_router(heroes_router)
app.include_router(teams_router)

@app.get("/")
def health():
    return {"status": "ok"}
