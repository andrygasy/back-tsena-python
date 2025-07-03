from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import ProductPage, ProductBase, ProductCreate, ProductUpdate
from app.services import products as product_service
from app.services.auth import get_current_user, is_professional, is_admin
from app.models import User
from app.services import minio_service


router = APIRouter()

@router.post("/api/products", response_model=ProductBase, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    files: Optional[List[UploadFile]] = File(None),
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.is_professional:
        product_in.user_id = current_user.id
    else:
        product_in.user_id = None
    if files:
        image_urls = []
        for file in files:
            url = minio_service.upload_file(file)
            if url:
                image_urls.append(url)
        product_in.images = image_urls
    return product_service.create(session, product_in)


@router.put("/api/products/{product_id}", response_model=ProductBase)
async def update_product(
    product_id: UUID,
    product_in: ProductUpdate,
    files: Optional[List[UploadFile]] = File(None),
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = product_service.find_one(session, product_id)
    if current_user.role != "admin" and product.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if files:
        # Delete old images
        if product.images:
            for image_url in product.images:
                object_name = image_url.split("/")[-1]
                minio_service.delete_file(object_name)
        # Upload new images
        image_urls = []
        for file in files:
            url = minio_service.upload_file(file)
            if url:
                image_urls.append(url)
        product_in.images = image_urls

    return product_service.update(session, product_id, product_in)


@router.delete("/api/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = product_service.find_one(session, product_id)
    if current_user.role != "admin" and product.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if product.images:
        for image_url in product.images:
            object_name = image_url.split("/")[-1]
            minio_service.delete_file(object_name)

    product_service.remove(session, product_id)
    return


@router.get("/api/products", response_model=ProductPage)
async def list_products(
    page: int = 1,
    limit: int = 12,
    category_id: Optional[UUID] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    session: Session = Depends(get_db),
):
    products, total = product_service.find_all_public(
        session, page, limit, category_id, search, min_price, max_price
    )
    return {"products": products, "total": total, "page": page, "limit": limit}

@router.get("/api/products/{product_id}", response_model=ProductBase)
async def get_product(product_id: UUID, session: Session = Depends(get_db)):
    return product_service.find_one(session, product_id)
