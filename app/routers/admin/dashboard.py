from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import require_role
from app.services import dashboard as dashboard_service

router = APIRouter()

@router.get("/api/admin/dashboard")
async def get_dashboard(
    session: Session = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    return dashboard_service.get_stats(session)
