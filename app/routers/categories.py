from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import CategoryPage, CategoryBase, CategoryTree, CategoryCreate, CategoryUpdate
from app.services import categories as category_service
from app.services.auth import is_admin
from app.models import User

router = APIRouter()

@router.post("/api/categories", response_model=CategoryBase, status_code=status.HTTP_201_CREATED, dependencies=[Depends(is_admin)])
async def create_category(
    category_in: CategoryCreate,
    session: Session = Depends(get_db),
):
    return category_service.create(session, category_in)


@router.put("/api/categories/{category_id}", response_model=CategoryBase, dependencies=[Depends(is_admin)])
async def update_category(
    category_id: UUID,
    category_in: CategoryUpdate,
    session: Session = Depends(get_db),
):
    return category_service.update(session, category_id, category_in)


@router.delete("/api/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_admin)])
async def delete_category(
    category_id: UUID,
    session: Session = Depends(get_db),
):
    category_service.remove(session, category_id)
    return


@router.get("/api/categories", response_model=CategoryPage)
async def list_categories(
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    session: Session = Depends(get_db),
):
    categories, total = category_service.find_all(session, page, limit, search)
    return {"categories": categories, "total": total, "page": page, "limit": limit}

@router.get("/api/categories/{category_id}", response_model=CategoryBase)
async def get_category(
    category_id: UUID,
    session: Session = Depends(get_db),
):
    return category_service.find_one(session, category_id)

@router.get("/api/categories/tree", response_model=list[CategoryTree])
async def get_tree(session: Session = Depends(get_db)):
    return category_service.find_tree(session)
