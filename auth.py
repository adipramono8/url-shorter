import os
import crud, dbModel
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer 
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dbSetup import get_db
from schemas import TokenData, UserResponse

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing setup
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password[:72])

# JWT token creation
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# FastAPI  depedency for "Get Current User"
# Getting token and Database
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) 
    try:
        # Decode JWT token 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        # Checking bad token
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # If token is valid, get the user from DB
    user = crud.get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user