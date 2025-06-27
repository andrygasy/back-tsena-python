from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas import CategoryBase, CategoryCreate, CategoryUpdate
from app.services import categories as category_service
from app.core.dependencies import require_role

router = APIRouter()

@router.post("/api/admin/categories", response_model=CategoryBase, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    return await category_service.create(session, data)

@router.put("/api/admin/categories/{category_id}", response_model=CategoryBase)
async def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    return await category_service.update(session, category_id, data)

@router.delete("/api/admin/categories/{category_id}")
async def delete_category(
    category_id: UUID,
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    await category_service.remove(session, category_id)
    return {"message": "Catégorie supprimée avec succès."}
