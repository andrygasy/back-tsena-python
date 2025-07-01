from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, func, update, delete
from sqlalchemy.orm import Session

from app.models import Category

def find_all(
    session: Session,
    page: int,
    limit: int,
    search: Optional[str] = None,
) -> Tuple[List[Category], int]:
    query = select(Category)
    if search:
        term = f"%{search}%"
        query = query.where(Category.name.ilike(term))
    count_query = select(func.count()).select_from(query.subquery())
    total = session.scalar(count_query)
    result = session.execute(
        query.order_by(Category.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    return result.scalars().all(), total or 0

def find_one(session: Session, category_id: UUID) -> Category:
    result = session.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")
    return category

def create(session: Session, data) -> Category:
    category = Category(**data.dict())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

def update(session: Session, category_id: UUID, data) -> Category:
    result = session.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(category, key, value)
    session.commit()
    session.refresh(category)
    return category

def remove(session: Session, category_id: UUID, soft_delete: bool = True) -> None:
    result = session.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")
    session.delete(category)
    session.commit()

def find_tree(session: Session) -> List[dict]:
    result = session.execute(select(Category))
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
