from fastapi import APIRouter

from . import auth, profile, categories
from .admin import users as admin_users, categories as admin_categories

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, tags=["profile"])
api_router.include_router(categories.router, tags=["categories"])
api_router.include_router(admin_users.router, tags=["admin"])
api_router.include_router(admin_categories.router, tags=["admin"])
__all__ = ["api_router", "auth", "profile", "categories", "admin_users", "admin_categories"]
