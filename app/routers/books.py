from fastapi import APIRouter, Depends, HTTPException, Path
from app.config import Settings, get_settings
from app.db.database import get_db
from app.db.models import Books
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/book',
    tags=['book']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class BookRequest(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    published_date: int = Field(gt=0, lt=2026)

@router.get("/ping")
def hello(settings: Settings = Depends(get_settings)):
    return {
        "msg": "Hello World!",
        "environment": settings.environment,
        "testing": settings.testing
        }

@router.get('/all', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Books).filter(Books.visibility == 'public').all()

@router.get('/allmybooks', status_code=status.HTTP_200_OK)
async def read_all_mybook(user: user_dependency, db: db_dependency):
    return db.query(Books).filter(Books.owner_id == user.id).all()

@router.get('/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(db: db_dependency, book_id: int = Path(gt=0)):
    book = db.query(Books).filter(Books.id == book_id).first()
    if book is not None:
        return book
    raise HTTPException(status_code=404, detail='Book Not Found')

@router.post('/add', status_code=status.HTTP_201_CREATED)
async def create_book(user: user_dependency, db: db_dependency, book_request: BookRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Auth Failed')
    book_model = Books(**book_request.model_dump(), owner_id=user.get('id'))

    db.add(book_model)
    db.commit()

@router.put('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(user: user_dependency, db: db_dependency, book_request: BookRequest, book_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Auth Failed')
    book_model = db.query(Books).filter(Books.owner_id == user.get('id')).filter(Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book Not Found")
    
    book_model.title = book_request.title
    book_model.author = book_request.author
    book_model.description = book_request.description
    book_model.published_date =  book_request.published_date
    book_model.verified = False

    db.add(book_model)
    db.commit()

@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(user: user_dependency, db: db_dependency, book_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Auth Failed')
    book_model = db.query(Books).filter(Books.owner_id == user.get('id')).filter(Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book Not Found")
    db.query(Books).filter(Books.owner_id == user.get('id')).filter(Books.id == book_id).delete()
    db.commit()