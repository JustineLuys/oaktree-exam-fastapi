import os

from typing import Annotated
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import  timedelta, datetime, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
from pydantic import BaseModel
from starlette import status

load_dotenv()
SECRET_KEY= os.getenv('SECRET_KEY')
ALGORITHM= os.getenv('ALGORITHM')

class Token(BaseModel):
    access_token: str
    token_type: str
    
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer  = OAuth2PasswordBearer(tokenUrl='signin')

def hash_password(plaintext: str):
    return bcrypt_context.hash(plaintext)

def compare_password(plaintext: str, hash: str):
    return bcrypt_context.verify(plaintext, hash)

def assign_jwt(username: str, user_id: int, expires_delta: timedelta):
    payload = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({'exp': expires})
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        return {'username': username, 'id': user_id}
    except JWTError:
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        