from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import UserCreate, UserOut, Token
from app.services import auth as auth_service


router = APIRouter()

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, session: Session = Depends(get_db)):
    existing = auth_service.get_user_by_email(session, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = auth_service.create_user(session, user_in.name, user_in.email, user_in.password)
    user_data = UserOut.from_orm(user).dict()
    user_data["id"] = str(user_data["id"])
    token = auth_service.create_access_token({"sub": str(user.id), "user": user_data})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user_in: UserCreate, session: Session = Depends(get_db)):
    user = auth_service.authenticate_user(session, user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_data = UserOut.from_orm(user).dict()
    user_data["id"] = str(user_data["id"])
    token = auth_service.create_access_token({"sub": str(user.id), "user": user_data})
    return {"access_token": token, "token_type": "bearer"}
