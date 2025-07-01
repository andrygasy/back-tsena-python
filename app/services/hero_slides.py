from typing import List, Tuple
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models import HeroSlide

async def find_all(session: AsyncSession, page: int, limit: int) -> Tuple[List[HeroSlide], int]:
    query = select(HeroSlide)
    count = await session.scalar(select(func.count()).select_from(query.subquery()))
    result = await session.execute(
        query.order_by(HeroSlide.order).offset((page - 1) * limit).limit(limit)
    )
    return result.scalars().all(), count or 0

async def find_one(session: AsyncSession, slide_id: UUID) -> HeroSlide:
    result = await session.execute(select(HeroSlide).where(HeroSlide.id == slide_id))
    slide = result.scalars().first()
    if not slide:
        raise HTTPException(status_code=404, detail="Slide non trouvé.")
    return slide

async def create(session: AsyncSession, data) -> HeroSlide:
    slide = HeroSlide(**data.dict())
    session.add(slide)
    await session.commit()
    await session.refresh(slide)
    return slide

async def update(session: AsyncSession, slide_id: UUID, data) -> HeroSlide:
    slide = await find_one(session, slide_id)
    for k, v in data.dict(exclude_unset=True).items():
        setattr(slide, k, v)
    await session.commit()
    await session.refresh(slide)
    return slide

async def remove(session: AsyncSession, slide_id: UUID) -> None:
    slide = await find_one(session, slide_id)
    await session.delete(slide)
    await session.commit()
