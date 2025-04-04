from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
from utils.auth import hash_password
from utils.queries import get_user_by_username_from_db
from models import Users

from utils.user_model import CreateUserRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency,
    create_user_request: CreateUserRequest):
    existing_user = get_user_by_username_from_db(db, create_user_request.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    new_user = Users(
        full_name = create_user_request.full_name,
        username = create_user_request.username,
        hashed_password = hash_password(create_user_request.password)
    )
    db.add(new_user)
    db.commit()