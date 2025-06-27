from typing import Optional, Tuple, List

from sqlalchemy.future import select
from sqlalchemy import update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models import User

async def find_all(
    session: AsyncSession,
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
    total = await session.scalar(count_query)
    result = await session.execute(query.offset((page - 1) * limit).limit(limit))
    return result.scalars().all(), total or 0

async def update_status(session: AsyncSession, user_id: int, status: str, reason: str) -> None:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    user.status = status
    await session.commit()

async def update_role(session: AsyncSession, user_id: int, role: str, permissions: Optional[list]) -> None:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    user.role = role
    await session.commit()

async def remove(session: AsyncSession, user_id: int) -> None:
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()

async def update_profile(session: AsyncSession, user_id: int, name: str, phone: Optional[str], avatar: Optional[str]) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    user.name = name
    user.phone = phone
    user.avatar = avatar
    await session.commit()
    await session.refresh(user)
    return user
