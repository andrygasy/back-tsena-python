from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.models.order import OrderStatus

class OrderItem(BaseModel):
    product_id: UUID
    quantity: int
    price: float

class OrderBase(BaseModel):
    id: UUID
    user_id: UUID
    items: List[OrderItem]
    total: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    items: List[OrderItem]

class OrderPage(BaseModel):
    orders: List[OrderBase]
    total: int
    page: int
    limit: int

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
