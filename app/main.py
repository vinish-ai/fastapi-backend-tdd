from fastapi import FastAPI, Depends, HTTPException, Path
from app.config import Settings, get_settings
from app.db.database import engine, get_db
from app.db import models
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/ping")
def hello(settings: Settings = Depends(get_settings)):
    return {
        "msg": "Hello World!",
        "environment": settings.environment,
        "testing": settings.testing
        }

@app.get('/book/all', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(models.Books).all()

@app.get('/book/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(db: db_dependency, book_id: int = Path(gt=0)):
    book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book is not None:
        return book
    raise HTTPException(status_code=404, detail='Book Not Found')