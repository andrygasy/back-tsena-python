from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas import ProductPage, ProductBase
from app.services import products as product_service

router = APIRouter()

@router.get("/api/products", response_model=ProductPage)
async def list_products(
    page: int = 1,
    limit: int = 12,
    category_id: Optional[UUID] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    session: AsyncSession = Depends(get_session),
):
    products, total = await product_service.find_all_public(
        session, page, limit, category_id, search, min_price, max_price
    )
    return {"products": products, "total": total, "page": page, "limit": limit}

@router.get("/api/products/{product_id}", response_model=ProductBase)
async def get_product(product_id: UUID, session: AsyncSession = Depends(get_session)):
    return await product_service.find_one(session, product_id)
