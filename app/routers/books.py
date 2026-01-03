from fastapi import APIRouter, HTTPException,status, Query, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models
from app.dependencies import get_db
from ..schemas import BookCreate, BookUpdate, BookResponse
from app import schemas

router = APIRouter(prefix="/books",tags=["Books"])


@router.get("/search", status_code=status.HTTP_200_OK, response_model=List[schemas.BookResponse])
def search_books(search: str, db: Session = Depends(get_db)):
    books = db.query(models.Book).filter(
        models.Book.title.ilike(f"%{search}%") |
        models.Book.author.ilike(f"%{search}%")
    ).all()

    if not books:
        raise HTTPException(status_code=404,detail="No books found matching your search")

    return books


@router.get("/filter", status_code=status.HTTP_200_OK, response_model=List[schemas.BookResponse])
def filter_books(
    min_year: int = Query(0, ge=0),
    max_year: int | None = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)

    if min_year:
        query = query.filter(models.Book.year >= min_year)

    if max_year:
        query = query.filter(models.Book.year <= max_year)

    books = query.all()

    if not books:
        raise HTTPException(
            status_code=404,
            detail="No books found with given filters"
        )

    return books


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


@router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", status_code=status.HTTP_200_OK, response_model=BookResponse)
def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_data.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"detail": "Book deleted"}
