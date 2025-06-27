from fastapi import APIRouter

from . import auth, profile
from .admin import users as admin_users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, tags=["profile"])
api_router.include_router(admin_users.router, tags=["admin"])
__all__ = ["api_router", "auth", "profile", "admin_users"]
