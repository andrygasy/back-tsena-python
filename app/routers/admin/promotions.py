from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas import (
    PromotionBase,
    PromotionCreate,
    PromotionUpdate,
    PromotionPage,
)
from app.services import promotions as service
from app.core.dependencies import require_role

router = APIRouter()

@router.get("/api/admin/promotions", response_model=PromotionPage)
async def list_promotions(
    page: int = 1,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    promos, total = await service.find_all(session, page, limit)
    return {"promotions": promos, "total": total, "page": page, "limit": limit}

@router.get("/api/admin/promotions/{promo_id}", response_model=PromotionBase)
async def get_promo(
    promo_id: UUID,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    return await service.find_one(session, promo_id)

@router.post("/api/admin/promotions", response_model=PromotionBase, status_code=status.HTTP_201_CREATED)
async def create_promo(
    data: PromotionCreate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    return await service.create(session, data)

@router.put("/api/admin/promotions/{promo_id}", response_model=PromotionBase)
async def update_promo(
    promo_id: UUID,
    data: PromotionUpdate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    return await service.update(session, promo_id, data)

@router.delete("/api/admin/promotions/{promo_id}")
async def delete_promo(
    promo_id: UUID,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    await service.remove(session, promo_id)
    return {"message": "Promotion supprimée"}
