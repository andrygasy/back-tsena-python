from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.product import ProductStatus

class ProductBase(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[UUID] = None
    user_id: Optional[int] = None
    images: Optional[List[str]] = None
    stock: int
    status: ProductStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[UUID] = None
    user_id: Optional[int] = None
    images: Optional[List[str]] = None
    stock: int
    status: Optional[ProductStatus] = ProductStatus.pending

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[UUID] = None
    images: Optional[List[str]] = None
    stock: Optional[int] = None
    status: Optional[ProductStatus] = None

class ProductPage(BaseModel):
    products: List[ProductBase]
    total: int
    page: int
    limit: int

class StatusUpdate(BaseModel):
    status: ProductStatus
    reason: Optional[str] = None
