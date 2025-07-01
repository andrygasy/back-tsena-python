from datetime import datetime
from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, constr, confloat

from app.models.promotion import PromotionDiscountType


class PromotionConditions(BaseModel):
    minAmount: Optional[float] = None
    categories: Optional[List[str]] = None
    maxUsage: Optional[int] = None

class PromotionBase(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    discount_type: PromotionDiscountType
    discount_value: float
    start_date: datetime
    end_date: datetime
    conditions: Optional[PromotionConditions] = None
    is_active: bool
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PromotionCreate(BaseModel):
    name: constr(min_length=1)
    description: Optional[str] = None
    discount_type: PromotionDiscountType
    discount_value: confloat(gt=0)
    start_date: datetime
    end_date: datetime
    conditions: Optional[PromotionConditions] = None
    is_active: bool

class PromotionUpdate(BaseModel):
    name: Optional[constr(min_length=1)] = None
    description: Optional[str] = None
    discount_type: Optional[PromotionDiscountType] = None
    discount_value: Optional[confloat(gt=0)] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    conditions: Optional[PromotionConditions] = None
    is_active: Optional[bool] = None

class PromotionPage(BaseModel):
    promotions: List[PromotionBase]
    total: int
    page: int
    limit: int
