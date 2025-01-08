from fastapi import FastAPI, Depends
from app.config import Settings, get_settings
from app.db.database import engine, get_db
from app.db import models
from typing import Annotated
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/ping")
def hello(settings: Settings = Depends(get_settings)):
    return {
        "msg": "Hello World!",
        "environment": settings.environment,
        "testing": settings.testing
        }

@app.get('/')
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Books).all()