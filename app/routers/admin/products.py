from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import (
    ProductBase,
    ProductUpdate,
    ProductPage,
    ProductStatusUpdate,
)
from app.services import products as product_service
from app.core.dependencies import require_role

router = APIRouter()

@router.get("/api/admin/products", response_model=ProductPage)
async def list_products(
    page: int = 1,
    limit: int = 20,
    status: Optional[str] = None,
    category_id: Optional[UUID] = None,
    user_id: Optional[UUID] = None,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    products, total = product_service.find_all_public(
        session, page, limit, category_id
    )
    if status:
        products = [p for p in products if p.status == status]
    if user_id:
        products = [p for p in products if p.user_id == user_id]
    return {"products": products, "total": total, "page": page, "limit": limit}

@router.put("/api/admin/products/{product_id}/status", response_model=ProductBase)
async def change_status(
    product_id: UUID,
    data: ProductStatusUpdate,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    return product_service.update_status(session, product_id, data.status.value, data.reason)

@router.put("/api/admin/products/{product_id}", response_model=ProductBase)
async def update_product(
    product_id: UUID,
    data: ProductUpdate,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    return product_service.update(session, product_id, data)

@router.delete("/api/admin/products/{product_id}")
async def delete_product(
    product_id: UUID,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    product_service.remove(session, product_id)
    return {"message": "Produit supprimé"}
