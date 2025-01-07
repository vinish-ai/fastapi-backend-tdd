from fastapi import FastAPI, Depends
from app.config import Settings, get_settings
from app.db.database import engine
from app.db import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/ping")
def hello(settings: Settings = Depends(get_settings)):
    return {
        "msg": "Hello World!",
        "environment": settings.environment,
        "testing": settings.testing
        }