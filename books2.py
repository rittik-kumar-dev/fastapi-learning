from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Optional
app=FastAPI()
class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    
    
    def __init__(self,id,title,author,description,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating

class Book_request(BaseModel):
        id: Optional[int]=None
        title:str =Field(min_length=3)
        author:str  =Field(min_length=3)
        description:str =Field(min_length=3)
        rating:int  =Field(gt=-1,lt=6)
        model_config={
    "json_schema_extra":{
        "example":{
            "title":" coding with rittik",
            "author":" zang lu",
            "description":"a new description of book",
            "rating":"5"
            
        }
    }
}
    
    

    
        
BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]
@app.get("/books")
async def read_all_books():
    return BOOKS 
 
@app.get("/books/{book_id}")
async def get_book(book_id:int):
    for book in BOOKS:
        if book.id==book_id:
            return book;

@app.get("/books/")
async def read_by_rating(rating_value:int):
    for book in BOOKS:
        if book.rating==rating_value:
            return book
        
@app.put("/books/update_book")
async def update_book(book:Book_request):
     for i in range(len(BOOKS)):
         if BOOKS[i].id==book.id:
            BOOKS[i]=book       
        
@app.post("/create_book")
async def create_book(bookrequest:Book_request):
    new_book=Book(**bookrequest.model_dump())
    
    BOOKS.append(find_book_id(new_book))
    return new_book

#id increment 
def find_book_id(book:Book):
    if len(BOOKS)>0:
        book.id=BOOKS[-1].id+1
    else:
        book.id=1
    return book



@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].title.casefold()==book_title.casefold():
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
        return {"message": "Book not found"}


        
