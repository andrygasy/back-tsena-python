import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    name : str
    email: str
    password: str

class UserOut(BaseModel):
    id: UUID
    name: Optional[str]
    email: str
    role: str
    status: str
    phone: Optional[str]
    avatar: Optional[str]
    is_professional: bool
    professional_type: Optional[str]

    class Config:
        orm_mode = True

    @validator('id', pre=True, allow_reuse=True)
    def uuid_to_str(cls, v):
        return str(v)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str
