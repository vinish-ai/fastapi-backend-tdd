from fastapi import FastAPI
from app.db.database import engine
from app.db import models
from app.routers import books, auth, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(books.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)