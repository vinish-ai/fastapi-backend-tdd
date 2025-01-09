from fastapi import FastAPI, Depends, HTTPException, Path
from app.config import Settings, get_settings
from app.db.database import engine, get_db
from app.db import models
from app.db.models import Books
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

class BookRequest(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    published_date: int = Field(gt=0, lt=2026)

@app.get("/ping")
def hello(settings: Settings = Depends(get_settings)):
    return {
        "msg": "Hello World!",
        "environment": settings.environment,
        "testing": settings.testing
        }

@app.get('/book/all', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Books).all()

@app.get('/book/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(db: db_dependency, book_id: int = Path(gt=0)):
    book = db.query(Books).filter(Books.id == book_id).first()
    if book is not None:
        return book
    raise HTTPException(status_code=404, detail='Book Not Found')

@app.post('/book/add', status_code=status.HTTP_201_CREATED)
async def create_book(db: db_dependency, book_request: BookRequest):
    book_model = Books(**book_request.model_dump())

    db.add(book_model)
    db.commit()