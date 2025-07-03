from typing import Optional, Tuple, List
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy import update, delete, func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import User

def find_all(
    session: Session,
    page: int,
    limit: int,
    role: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> Tuple[List[User], int]:
    query = select(User)
    if role:
        query = query.where(User.role == role)
    if status:
        query = query.where(User.status == status)
    if search:
        term = f"%{search}%"
        query = query.where(User.name.ilike(term))
    count_query = select(func.count()).select_from(query.subquery())
    total = session.scalar(count_query)
    result = session.execute(query.offset((page - 1) * limit).limit(limit))
    return result.scalars().all(), total or 0

def update_status(session: Session, user_id: UUID, status: str, reason: str) -> None:
    result = session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    user.status = status
    session.commit()

def update_role(session: Session, user_id: UUID, role: str, permissions: Optional[list]) -> None:
    result = session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    user.role = role
    session.commit()

def remove(session: Session, user_id: UUID) -> None:
    session.execute(delete(User).where(User.id == user_id))
    session.commit()

def update_profile(session: Session, user_id: UUID, name: str, phone: Optional[str], avatar: Optional[str]) -> User:
    result = session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    user.name = name
    user.phone = phone
    user.avatar = avatar
    session.commit()
    session.refresh(user)
    return user
