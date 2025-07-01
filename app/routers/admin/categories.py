from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import CategoryBase, CategoryCreate, CategoryUpdate, CategoryPage
from app.services import categories as category_service
from app.core.dependencies import require_role

router = APIRouter()

@router.get("/api/admin/categories", response_model=CategoryPage)
async def list_categories_admin(
    page: int = 1,
    limit: int = 10,
    name: Optional[str] = None,
    include_inactive: bool = False,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    categories, total = category_service.find_all(session, page, limit, name)
    if not include_inactive:
        categories = [c for c in categories if getattr(c, "is_active", True)]
    return {"categories": categories, "total": total, "page": page, "limit": limit}

@router.get("/api/admin/categories/{category_id}", response_model=CategoryBase)
async def get_category_admin(
    category_id: UUID,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    return category_service.find_one(session, category_id)

@router.post("/api/admin/categories", response_model=CategoryBase, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    return category_service.create(session, data)

@router.put("/api/admin/categories/{category_id}", response_model=CategoryBase)
async def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    return category_service.update(session, category_id, data)

@router.delete("/api/admin/categories/{category_id}")
async def delete_category(
    category_id: UUID,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    category_service.remove(session, category_id)
    return {"message": "Catégorie supprimée avec succès."}
