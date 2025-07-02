from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from sqlalchemy.future import select


from app.models import User
from app.db.session import get_db

# OAuth2 scheme configuration for token retrieval from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY: str = "change-me"
ALGORITHM: str = "HS256"

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    result = session.execute(select(User).where(User.email == email))
    return result.scalars().first()

def create_user(session: Session, email: str, password: str) -> User:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(email=email, password_hash=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with an expiration time."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    Authorize: AuthJWT = Depends(),
    session: Session = Depends(get_db),
) -> User:
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = Authorize.get_jwt_subject()
    result = session.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
