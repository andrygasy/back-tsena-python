from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category

async def find_all(
    session: AsyncSession,
    page: int,
    limit: int,
    search: Optional[str] = None,
) -> Tuple[List[Category], int]:
    query = select(Category)
    if search:
        term = f"%{search}%"
        query = query.where(Category.name.ilike(term))
    count_query = select(func.count()).select_from(query.subquery())
    total = await session.scalar(count_query)
    result = await session.execute(
        query.order_by(Category.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    return result.scalars().all(), total or 0

async def find_one(session: AsyncSession, category_id: UUID) -> Category:
    result = await session.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")
    return category

async def create(session: AsyncSession, data) -> Category:
    category = Category(**data.dict())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category

async def update(session: AsyncSession, category_id: UUID, data) -> Category:
    result = await session.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(category, key, value)
    await session.commit()
    await session.refresh(category)
    return category

async def remove(session: AsyncSession, category_id: UUID, soft_delete: bool = True) -> None:
    result = await session.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")
    await session.delete(category)
    await session.commit()

async def find_tree(session: AsyncSession) -> List[dict]:
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    mapping = {c.id: {"id": str(c.id), "name": c.name, "description": c.description, "parent_id": str(c.parent_id) if c.parent_id else None, "children": []} for c in categories}
    roots = []
    for cat in categories:
        node = mapping[cat.id]
        if cat.parent_id:
            parent = mapping.get(cat.parent_id)
            if parent:
                parent["children"].append(node)
        else:
            roots.append(node)
    return roots
