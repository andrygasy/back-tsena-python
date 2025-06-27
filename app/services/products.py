from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, func, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product, ProductStatus

async def find_all_public(
    session: AsyncSession,
    page: int,
    limit: int,
    category_id: Optional[UUID] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> Tuple[List[Product], int]:
    query = select(Product).where(Product.status == ProductStatus.active.value)
    if category_id:
        query = query.where(Product.category_id == category_id)
    if search:
        term = f"%{search}%"
        query = query.where(or_(Product.name.ilike(term), Product.description.ilike(term)))
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    count_query = select(func.count()).select_from(query.subquery())
    total = await session.scalar(count_query)
    result = await session.execute(
        query.order_by(Product.created_at.desc()).offset((page - 1) * limit).limit(limit)
    )
    return result.scalars().all(), total or 0

async def find_one(session: AsyncSession, product_id: UUID) -> Product:
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé.")
    return product

async def create(session: AsyncSession, data) -> Product:
    product = Product(**data.dict())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product

async def update(session: AsyncSession, product_id: UUID, data) -> Product:
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé.")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    await session.commit()
    await session.refresh(product)
    return product

async def remove(session: AsyncSession, product_id: UUID) -> None:
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé.")
    await session.delete(product)
    await session.commit()

async def update_status(session: AsyncSession, product_id: UUID, status: str, reason: Optional[str]) -> Product:
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé.")
    product.status = status
    await session.commit()
    await session.refresh(product)
    return product
