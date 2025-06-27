from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas import OrderBase, OrderPage, OrderStatusUpdate
from app.services import orders as order_service
from app.core.dependencies import require_role
from app.models.order import OrderStatus

router = APIRouter()

@router.get("/api/admin/orders", response_model=OrderPage)
async def list_orders_admin(
    page: int = 1,
    limit: int = 20,
    status: Optional[OrderStatus] = None,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    orders, total = await order_service.find_all_admin(session, page, limit, status)
    return {"orders": orders, "total": total, "page": page, "limit": limit}

@router.put("/api/admin/orders/{order_id}/status", response_model=OrderBase)
async def change_order_status(
    order_id: UUID,
    data: OrderStatusUpdate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    return await order_service.update_status(session, order_id, data.status)
