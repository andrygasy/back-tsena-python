from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

class CategoryBase(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[UUID] = None

class CategoryPage(BaseModel):
    categories: List[CategoryBase]
    total: int
    page: int
    limit: int

class CategoryTree(CategoryBase):
    children: List['CategoryTree'] = []

CategoryTree.update_forward_refs()
