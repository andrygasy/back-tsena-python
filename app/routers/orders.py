from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import OrderBase, OrderCreate, OrderPage
from app.services import orders as order_service
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/api/orders", response_model=OrderBase, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    session: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return order_service.create_order(session, user.id, data)

@router.get("/api/orders", response_model=OrderPage)
async def list_orders(
    page: int = 1,
    limit: int = 10,
    session: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    orders, total = order_service.find_all_by_user(session, user.id, page, limit)
    return {"orders": orders, "total": total, "page": page, "limit": limit}

@router.get("/api/orders/{order_id}", response_model=OrderBase)
async def get_order(
    order_id: UUID,
    session: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    order = order_service.find_one(session, order_id)
    if order.user_id != user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Accès refusé")
    return order
