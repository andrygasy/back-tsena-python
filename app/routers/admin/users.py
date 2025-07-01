from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import UserPage, StatusUpdate, RoleUpdate
from app.services import user_service
from app.core.dependencies import require_role

router = APIRouter()

@router.get("/api/admin/users", response_model=UserPage)
async def list_users(
    page: int = 1,
    limit: int = 10,
    role: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    users, total = user_service.find_all(session, page, limit, role, status, search)
    return {"users": users, "total": total, "page": page, "limit": limit}

@router.put("/api/admin/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    data: StatusUpdate,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    user_service.update_status(session, user_id, data.status, data.reason)
    return {"message": "Statut de l'utilisateur modifié avec succès."}

@router.put("/api/admin/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    data: RoleUpdate,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    user_service.update_role(session, user_id, data.role, data.permissions)
    return {"message": "Rôle de l'utilisateur modifié avec succès."}

@router.delete("/api/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    user_service.remove(session, user_id)
    return {"message": "Utilisateur supprimé avec succès."}
