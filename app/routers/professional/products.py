from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import ProductBase, ProductCreate, ProductUpdate, ProductPage
from app.services import products as product_service
from app.core.dependencies import require_role

router = APIRouter()

@router.post("/api/professional/products", response_model=ProductBase, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    session: Session = Depends(get_db),
    user=Depends(require_role("professional")),
):
    data.user_id = user.id
    return product_service.create(session, data)

@router.put("/api/professional/products/{product_id}", response_model=ProductBase)
async def update_product(
    product_id: UUID,
    data: ProductUpdate,
    session: Session = Depends(get_db),
    user=Depends(require_role("professional")),
):
    product = product_service.find_one(session, product_id)
    if product.user_id != user.id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    return product_service.update(session, product_id, data)

@router.delete("/api/professional/products/{product_id}")
async def delete_product(
    product_id: UUID,
    session: Session = Depends(get_db),
    user=Depends(require_role("professional")),
):
    product = product_service.find_one(session, product_id)
    if product.user_id != user.id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    product_service.remove(session, product_id)
    return {"message": "Produit supprimé"}

@router.get("/api/professional/products", response_model=ProductPage)
async def list_my_products(
    page: int = 1,
    limit: int = 10,
    session: Session = Depends(get_db),
    user=Depends(require_role("professional")),
):
    products, total = product_service.find_all_public(session, page, limit)
    products = [p for p in products if p.user_id == user.id]
    return {"products": products, "total": total, "page": page, "limit": limit}
