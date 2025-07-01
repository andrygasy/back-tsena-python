from datetime import datetime
from uuid import UUID
from typing import List

from pydantic import BaseModel

class PromotionBase(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    discount_type: str
    value: float
    start_date: datetime
    end_date: datetime
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PromotionCreate(BaseModel):
    name: str
    description: str | None = None
    discount_type: str
    value: float
    start_date: datetime
    end_date: datetime
    active: bool = True

class PromotionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    discount_type: str | None = None
    value: float | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    active: bool | None = None

class PromotionPage(BaseModel):
    promotions: List[PromotionBase]
    total: int
    page: int
    limit: int
