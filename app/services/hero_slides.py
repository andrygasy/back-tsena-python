from typing import List, Tuple
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import HeroSlide

def find_all(session: Session, page: int, limit: int) -> Tuple[List[HeroSlide], int]:
    query = select(HeroSlide)
    count = session.scalar(select(func.count()).select_from(query.subquery()))
    result = session.execute(
        query.order_by(HeroSlide.order).offset((page - 1) * limit).limit(limit)
    )
    return result.scalars().all(), count or 0

def find_one(session: Session, slide_id: UUID) -> HeroSlide:
    result = session.execute(select(HeroSlide).where(HeroSlide.id == slide_id))
    slide = result.scalars().first()
    if not slide:
        raise HTTPException(status_code=404, detail="Slide non trouvé.")
    return slide

def create(session: Session, data) -> HeroSlide:
    slide = HeroSlide(**data.dict())
    session.add(slide)
    session.commit()
    session.refresh(slide)
    return slide

def update(session: Session, slide_id: UUID, data) -> HeroSlide:
    slide = find_one(session, slide_id)
    for k, v in data.dict(exclude_unset=True).items():
        setattr(slide, k, v)
    session.commit()
    session.refresh(slide)
    return slide

def remove(session: Session, slide_id: UUID) -> None:
    slide = find_one(session, slide_id)
    session.delete(slide)
    session.commit()
