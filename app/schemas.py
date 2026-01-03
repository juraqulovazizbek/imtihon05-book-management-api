from pydantic import BaseModel, Field
from typing import Optional, Annotated


class BookCreate(BaseModel):
    title: Annotated[str, Field(max_length=100)]
    author: Annotated[str, Field(max_length=100)]
    genre: Optional[Annotated[str, Field(max_length=100)]] = None
    year: Optional[int] = None
    rating: Optional[Annotated[float, Field(ge=0, le=5)]] = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None

    class Config:
        from_attributes = True


class BookUpdate(BaseModel):
    title: Optional[Annotated[str, Field(max_length=100)]] = None
    author: Optional[Annotated[str, Field(max_length=100)]] = None
    genre: Optional[Annotated[str, Field(max_length=100)]] = None
    year: Optional[int] = None
    rating: Optional[Annotated[float, Field(ge=0, le=5)]] = None
