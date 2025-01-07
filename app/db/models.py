from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    published_date = Column(Integer)
    verified = Column(Boolean, default=False)
    vector_indexed = Column(Boolean, default=False)