from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
from utils.queries import get_user_by_username_from_db
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth import compare_password
from utils.auth import assign_jwt, Token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/signin', response_model=Token, status_code=status.HTTP_200_OK)
async def signin_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency):
    
    existing_user = get_user_by_username_from_db(db, form_data.username)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")
    
    is_match = compare_password(form_data.password, existing_user.hashed_password)
    if not is_match:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    token = assign_jwt(existing_user.username, existing_user.id, timedelta(days=30))
    
    return {'access_token': token, 'token_type': 'bearer'}