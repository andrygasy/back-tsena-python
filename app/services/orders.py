from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order, OrderStatus
from app.schemas.orders import OrderCreate, OrderItem

async def create_order(
    session: AsyncSession, user_id: int, data: OrderCreate
) -> Order:
    items = [item.dict() for item in data.items]
    total = sum(item["price"] * item["quantity"] for item in items)
    order = Order(user_id=user_id, items=items, total=total)
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order

async def find_all_by_user(
    session: AsyncSession,
    user_id: int,
    page: int,
    limit: int,
) -> Tuple[List[Order], int]:
    query = select(Order).where(Order.user_id == user_id)
    count = await session.scalar(select(func.count()).select_from(query.subquery()))
    result = await session.execute(
        query.order_by(Order.created_at.desc()).offset((page - 1) * limit).limit(limit)
    )
    return result.scalars().all(), count or 0

async def find_all_admin(
    session: AsyncSession,
    page: int,
    limit: int,
    status: Optional[OrderStatus] = None,
) -> Tuple[List[Order], int]:
    query = select(Order)
    if status:
        query = query.where(Order.status == status.value)
    count = await session.scalar(select(func.count()).select_from(query.subquery()))
    result = await session.execute(
        query.order_by(Order.created_at.desc()).offset((page - 1) * limit).limit(limit)
    )
    return result.scalars().all(), count or 0

async def find_one(session: AsyncSession, order_id: UUID) -> Order:
    result = await session.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée.")
    return order

async def update_status(
    session: AsyncSession, order_id: UUID, status: OrderStatus
) -> Order:
    order = await find_one(session, order_id)
    order.status = status.value
    await session.commit()
    await session.refresh(order)
    return order
