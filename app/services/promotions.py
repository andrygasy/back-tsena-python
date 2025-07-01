from typing import List, Tuple
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models import Promotion

async def find_all(session: AsyncSession, page: int, limit: int) -> Tuple[List[Promotion], int]:
    query = select(Promotion)
    count = await session.scalar(select(func.count()).select_from(query.subquery()))
    result = await session.execute(
        query.order_by(Promotion.created_at.desc()).offset((page - 1) * limit).limit(limit)
    )
    return result.scalars().all(), count or 0

async def find_one(session: AsyncSession, promotion_id: UUID) -> Promotion:
    result = await session.execute(select(Promotion).where(Promotion.id == promotion_id))
    promo = result.scalars().first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promotion non trouvée.")
    return promo

async def create(session: AsyncSession, data) -> Promotion:
    if data.start_date >= data.end_date:
        raise HTTPException(status_code=400, detail="Invalid dates")
    promo = Promotion(**data.dict())
    session.add(promo)
    await session.commit()
    await session.refresh(promo)
    return promo

async def update(session: AsyncSession, promotion_id: UUID, data) -> Promotion:
    promo = await find_one(session, promotion_id)
    update_data = data.dict(exclude_unset=True)
    if "start_date" in update_data and "end_date" in update_data:
        if update_data["start_date"] >= update_data["end_date"]:
            raise HTTPException(status_code=400, detail="Invalid dates")
    for k, v in update_data.items():
        setattr(promo, k, v)
    await session.commit()
    await session.refresh(promo)
    return promo

async def remove(session: AsyncSession, promotion_id: UUID) -> None:
    promo = await find_one(session, promotion_id)
    await session.delete(promo)
    await session.commit()
