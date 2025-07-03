from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from uuid import UUID


from app.models import User
from app.db.session import get_db
from app.schemas import TokenData

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

# Fonction pour vérifier un token JWT et extraire les infos
def verify_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return TokenData(user_id=user_id)
    except PyJWTError:
        raise credentials_exception

def get_current_user(
    token_data: TokenData = Depends(verify_token),
    session: Session = Depends(get_db),
) -> User:
    result = session.execute(select(User).where(User.id == UUID(token_data.user_id)))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

def is_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def is_professional(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_professional:
        raise HTTPException(status_code=403, detail="User is not a professional")
    return current_user
