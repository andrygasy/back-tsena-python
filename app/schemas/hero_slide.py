from datetime import datetime
from uuid import UUID
from typing import List

from pydantic import BaseModel

class HeroSlideBase(BaseModel):
    id: UUID
    title: str
    image_url: str
    link_url: str | None = None
    order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class HeroSlideCreate(BaseModel):
    title: str
    image_url: str
    link_url: str | None = None
    order: int = 0
    is_active: bool = True

class HeroSlideUpdate(BaseModel):
    title: str | None = None
    image_url: str | None = None
    link_url: str | None = None
    order: int | None = None
    is_active: bool | None = None

class HeroSlidePage(BaseModel):
    slides: List[HeroSlideBase]
    total: int
    page: int
    limit: int
