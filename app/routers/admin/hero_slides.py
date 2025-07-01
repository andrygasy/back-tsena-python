from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas import (
    HeroSlideBase,
    HeroSlideCreate,
    HeroSlideUpdate,
    HeroSlidePage,
)
from app.services import hero_slides as service
from app.core.dependencies import require_role

router = APIRouter()

@router.get("/api/admin/hero-slides", response_model=HeroSlidePage)
async def list_slides(
    page: int = 1,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    slides, total = await service.find_all(session, page, limit)
    return {"slides": slides, "total": total, "page": page, "limit": limit}

@router.get("/api/admin/hero-slides/{slide_id}", response_model=HeroSlideBase)
async def get_slide(
    slide_id: UUID,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    return await service.find_one(session, slide_id)

@router.post("/api/admin/hero-slides", response_model=HeroSlideBase, status_code=status.HTTP_201_CREATED)
async def create_slide(
    data: HeroSlideCreate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    return await service.create(session, data)

@router.put("/api/admin/hero-slides/{slide_id}", response_model=HeroSlideBase)
async def update_slide(
    slide_id: UUID,
    data: HeroSlideUpdate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    return await service.update(session, slide_id, data)

@router.delete("/api/admin/hero-slides/{slide_id}")
async def delete_slide(
    slide_id: UUID,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    await service.remove(session, slide_id)
    return {"message": "Slide supprimé"}
