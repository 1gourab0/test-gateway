from fastapi import FastAPI, HTTPException, Path, Body
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Model for a book
class Book(BaseModel):
    id: int
    author: str
    name: str
    status: str

# Model for adding or updating a book
class BookInput(BaseModel):
    author: str
    name: str
    status: str

books: List[Book] = []

# Helper function to generate IDs
def generate_id():
    return len(books) + 1

# Endpoint to get all books
@app.get("/reading-list/books", response_model=List[Book])
def get_books():
    return books

# Endpoint to add a new book
@app.post("/reading-list/books", response_model=Book)
def add_book(book: BookInput):
    new_book = Book(
        id=generate_id(),
        author=book.author,
        name=book.name,
        status=book.status
    )
    books.append(new_book)
    return new_book

# Endpoint to get a book by ID
@app.get("/reading-list/books/{book_id}", response_model=Book)
def get_book(book_id: int = Path(..., title="The ID of the book to retrieve")):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Endpoint to delete a book by ID
@app.delete("/reading-list/books/{book_id}", status_code=204)
def delete_book(book_id: int = Path(..., title="The ID of the book to delete")):
    global books
    books = [book for book in books if book.id != book_id]
    return

# Endpoint to update a book's status by ID
@app.put("/reading-list/books/{book_id}", response_model=Book)
def update_book_status(
    book_id: int = Path(..., title="The ID of the book to update"),
    status: str = Body(..., embed=True, title="The new status of the book")
):
    for book in books:
        if book.id == book_id:
            book.status = status
            return book
    raise HTTPException(status_code=404, detail="Book not found")
