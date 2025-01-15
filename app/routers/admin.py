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
    prefix='/admin',
    tags=['admin']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/book/all', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') !='admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Auth Failed')
    return db.query(Books).all()

@router.delete('/book/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(user: user_dependency, db: db_dependency, book_id: int = Path(gt=0)):
    if user is None or user.get('user_role') !='admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Auth Failed')
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book Not Found")
    db.query(Books).filter(Books.id == book_id).delete()
    db.commit()