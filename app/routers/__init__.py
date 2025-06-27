from fastapi import APIRouter

from . import auth, profile, categories, products
from .professional import products as professional_products
from .admin import users as admin_users, categories as admin_categories, products as admin_products

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, tags=["profile"])
api_router.include_router(categories.router, tags=["categories"])
api_router.include_router(products.router, tags=["products"])
api_router.include_router(admin_users.router, tags=["admin"])
api_router.include_router(admin_categories.router, tags=["admin"])
api_router.include_router(admin_products.router, tags=["admin"])
api_router.include_router(professional_products.router, tags=["professional"])
__all__ = [
    "api_router",
    "auth",
    "profile",
    "categories",
    "products",
    "admin_users",
    "admin_categories",
    "admin_products",
    "professional_products",
]
