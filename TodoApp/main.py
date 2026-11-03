from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
import models
from models import Todos
from database import engine, SessionLocal
from pydantic import BaseModel,Field
from starlette import status


app = FastAPI()

models.Base.metadata.create_all(bind=engine)
class Todo_request(BaseModel):
        
        title :str = Field(min_length=3)
        description :str= Field(min_length=3,max_length=100)
        priority :int=Field(gt=0,lt=6)
        complete : bool
        

def get_db():
    db=SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
@app.get("/")
def get_all(db:Session=Depends(get_db)):
    return db.query(models.Todos).all()

@app.get("/todo/{todos_id}")
def read_by_id(todos_id:int,db:Session=Depends(get_db)):
    todo_model= db.query(Todos).filter(Todos.id==todos_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail="not found")

@app.post("/create",status_code=201)
def create(todo_req:Todo_request,db:Session=Depends(get_db)):
    todo_model=Todos(**todo_req.model_dump())
    db.add(todo_model)
    db.commit()
    