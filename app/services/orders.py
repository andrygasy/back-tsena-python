from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Order, OrderStatus
from app.schemas.orders import OrderCreate, OrderItem

def create_order(
    session: Session, user_id: int, data: OrderCreate
) -> Order:
    items = [item.dict() for item in data.items]
    total = sum(item["price"] * item["quantity"] for item in items)
    order = Order(user_id=user_id, items=items, total=total)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def find_all_by_user(
    session: Session,
    user_id: int,
    page: int,
    limit: int,
) -> Tuple[List[Order], int]:
    query = select(Order).where(Order.user_id == user_id)
    count = session.scalar(select(func.count()).select_from(query.subquery()))
    result = session.execute(
        query.order_by(Order.created_at.desc()).offset((page - 1) * limit).limit(limit)
    )
    return result.scalars().all(), count or 0

def find_all_admin(
    session: Session,
    page: int,
    limit: int,
    status: Optional[OrderStatus] = None,
) -> Tuple[List[Order], int]:
    query = select(Order)
    if status:
        query = query.where(Order.status == status.value)
    count = session.scalar(select(func.count()).select_from(query.subquery()))
    result = session.execute(
        query.order_by(Order.created_at.desc()).offset((page - 1) * limit).limit(limit)
    )
    return result.scalars().all(), count or 0

def find_one(session: Session, order_id: UUID) -> Order:
    result = session.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée.")
    return order

def update_status(
    session: Session, order_id: UUID, status: OrderStatus
) -> Order:
    order = find_one(session, order_id)
    order.status = status.value
    session.commit()
    session.refresh(order)
    return order
