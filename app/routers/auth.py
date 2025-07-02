from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import UserCreate, UserOut, Token
from app.services import auth as auth_service

from fastapi.security import OAuth2PasswordBearer

router = APIRouter()


# OAuth2 scheme configuration for token retrieval from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, session: Session = Depends(get_db)):
    existing = auth_service.get_user_by_email(session, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = auth_service.create_user(session, user_in.email, user_in.password)
    return user

@router.post("/login", response_model=Token)
async def login(user_in: UserCreate, session: Session = Depends(get_db)):
    user = auth_service.authenticate_user(session, user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth_service.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
