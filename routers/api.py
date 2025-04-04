import os
from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from models import Items
from dotenv import load_dotenv
from database import SessionLocal
from utils.queries import *
from utils.auth import get_current_user

load_dotenv()

router = APIRouter(
    prefix = '/api',
    tags = ['/api']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class ItemRequest(BaseModel):
    name:str = Field(min_length=6, max_length =100)
    description: str = Field(max_length=100)
    price: int = Field(gt=0)

    model_config = {
        'json_schema_extra': {
            "example": {
                'name': 'My Item Name',
                'description': 'My Item Description',
                'price': 999
            }
        }
    }

@router.get('/items', status_code = status.HTTP_200_OK)
async def get_all_items(user: user_dependency, db: db_dependency):
    print(user)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    try:
        items_model = get_all_items_from_db(db, user.get('id'))  
        return {'data': items_model}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

@router.post('/items', status_code = status.HTTP_201_CREATED)
async def add_item(user: user_dependency, db: db_dependency, 
                   item_request: ItemRequest): 
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    new_item = Items(**item_request.model_dump(), owner_id = user.get('id'))
    db.add(new_item)
    db.commit()

@router.get('/items/{id}', status_code=status.HTTP_200_OK)
async def get_item(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    item_model = get_item_from_db(db, id, user.get('id'))
    if item_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} is not found")
    return {
        'data': item_model
    }

@router.put("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_item(user: user_dependency,
                      db: db_dependency, 
                      item_request:ItemRequest, 
                      id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    item_model = get_item_from_db(db, id, user.get('id'))
    if not item_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} is not found")
    
    item_model.name = item_request.name
    item_model.description = item_request.description
    item_model.price = item_request.price
    
    db.add(item_model)
    db.commit()

@router.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    user_id = user.get('id')
    item_model = get_item_from_db(db, id, user_id)
    
    if not item_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} is not found")
    
    delete_item_by_id_from_db(db, id, user_id)