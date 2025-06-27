from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas import CategoryPage, CategoryBase, CategoryTree
from app.services import categories as category_service

router = APIRouter()

@router.get("/api/categories", response_model=CategoryPage)
async def list_categories(
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    categories, total = await category_service.find_all(session, page, limit, search)
    return {"categories": categories, "total": total, "page": page, "limit": limit}

@router.get("/api/categories/{category_id}", response_model=CategoryBase)
async def get_category(
    category_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    return await category_service.find_one(session, category_id)

@router.get("/api/categories/tree", response_model=list[CategoryTree])
async def get_tree(session: AsyncSession = Depends(get_session)):
    return await category_service.find_tree(session)
