from fastapi import APIRouter, HTTPException,status, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models, database
from ..schemas import BookCreate, BookUpdate, BookResponse
from app import schemas
router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

# DB sessionni olish uchun
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE – yangi kitob qo‘shish
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# READ – barcha kitoblar
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

# READ – ID bo‘yicha kitob
@router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# UPDATE – kitobni yangilash
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

# DELETE – kitobni o‘chirish
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"detail": "Book deleted"}
