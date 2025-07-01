from typing import List, Tuple
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Promotion

def find_all(session: Session, page: int, limit: int) -> Tuple[List[Promotion], int]:
    query = select(Promotion)
    count = session.scalar(select(func.count()).select_from(query.subquery()))
    result = session.execute(
        query.order_by(Promotion.created_at.desc()).offset((page - 1) * limit).limit(limit)
    )
    return result.scalars().all(), count or 0

def find_one(session: Session, promotion_id: UUID) -> Promotion:
    result = session.execute(select(Promotion).where(Promotion.id == promotion_id))
    promo = result.scalars().first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promotion non trouvée.")
    return promo

def create(session: Session, data) -> Promotion:
    if data.start_date >= data.end_date:
        raise HTTPException(status_code=400, detail="Invalid dates")
    promo = Promotion(**data.dict())
    session.add(promo)
    session.commit()
    session.refresh(promo)
    return promo

def update(session: Session, promotion_id: UUID, data) -> Promotion:
    promo = find_one(session, promotion_id)
    update_data = data.dict(exclude_unset=True)
    if "start_date" in update_data and "end_date" in update_data:
        if update_data["start_date"] >= update_data["end_date"]:
            raise HTTPException(status_code=400, detail="Invalid dates")
    for k, v in update_data.items():
        setattr(promo, k, v)
    session.commit()
    session.refresh(promo)
    return promo

def remove(session: Session, promotion_id: UUID) -> None:
    promo = find_one(session, promotion_id)
    session.delete(promo)
    session.commit()
