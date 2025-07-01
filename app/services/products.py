from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, func, update, delete, or_
from sqlalchemy.orm import Session

from app.models import Product, ProductStatus

def find_all_public(
    session: Session,
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
    total = session.scalar(count_query)
    result = session.execute(
        query.order_by(Product.created_at.desc()).offset((page - 1) * limit).limit(limit)
    )
    return result.scalars().all(), total or 0

def find_one(session: Session, product_id: UUID) -> Product:
    result = session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé.")
    return product

def create(session: Session, data) -> Product:
    product = Product(**data.dict())
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def update(session: Session, product_id: UUID, data) -> Product:
    result = session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé.")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    session.commit()
    session.refresh(product)
    return product

def remove(session: Session, product_id: UUID) -> None:
    result = session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé.")
    session.delete(product)
    session.commit()

def update_status(session: Session, product_id: UUID, status: str, reason: Optional[str]) -> Product:
    result = session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé.")
    product.status = status
    session.commit()
    session.refresh(product)
    return product
