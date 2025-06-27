from typing import Literal, Optional, List, Dict

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product, Service

async def search(
    session: AsyncSession,
    query: str,
    search_type: Literal["products", "services", "all"] = "all",
    page: int = 1,
    limit: int = 10,
) -> Dict:
    q = (query or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Query must not be empty")

    ts_query = func.plainto_tsquery('french', q)
    products: List[Product] = []
    services: List[Service] = []
    total = 0

    if search_type in ("products", "all"):
        p_base = select(Product).where(
            func.to_tsvector('french', Product.name + ' ' + func.coalesce(Product.description, '')).op('@@')(ts_query)
        )
        count_query = select(func.count()).select_from(p_base.subquery())
        total_p = await session.scalar(count_query)
        result = await session.execute(
            p_base.order_by(Product.created_at.desc()).offset((page - 1) * limit).limit(limit)
        )
        products = result.scalars().all()
        total += total_p or 0

    if search_type in ("services", "all"):
        s_base = select(Service).where(
            func.to_tsvector('french', Service.name + ' ' + func.coalesce(Service.description, '')).op('@@')(ts_query)
        )
        count_query = select(func.count()).select_from(s_base.subquery())
        total_s = await session.scalar(count_query)
        result = await session.execute(
            s_base.order_by(Service.created_at.desc()).offset((page - 1) * limit).limit(limit)
        )
        services = result.scalars().all()
        total += total_s or 0

    return {
        "products": products if search_type in ("products", "all") else [],
        "services": services if search_type in ("services", "all") else [],
        "pagination": {"total": total, "page": page, "limit": limit},
    }

