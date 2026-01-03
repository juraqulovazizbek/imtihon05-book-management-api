from datetime import datetime
from app.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.orm import relationship
class Book(Base):
    __tablename__ = "books" 

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=100), nullable=False)
    author = Column(String(length=100), nullable=False)
    genre = Column(String(length=100), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    def __str__(self):
        return f"{self.title} by {self.author}"