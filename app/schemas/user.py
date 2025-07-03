from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class UserBase(BaseModel):
    id: UUID
    name: Optional[str]
    email: str
    role: str
    status: str
    created_at: datetime
    last_login: Optional[datetime]
    order_count: int
    total_spent: float
    phone: Optional[str]
    avatar: Optional[str]
    is_professional: bool
    professional_type: Optional[str]

    class Config:
        orm_mode = True

class UserPage(BaseModel):
    users: List[UserBase]
    total: int
    page: int
    limit: int

class StatusUpdate(BaseModel):
    status: str
    reason: Optional[str]

class RoleUpdate(BaseModel):
    role: str
    permissions: Optional[List[str]] = None

class ProfileOut(BaseModel):
    id: UUID
    name: Optional[str]
    email: str
    is_professional: bool
    professional_type: Optional[str]
    avatar: Optional[str]
    phone: Optional[str]

    class Config:
        orm_mode = True

class ProfileUpdate(BaseModel):
    name: str
    phone: Optional[str] = None
    avatar: Optional[str] = None
