from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.core.dependencies import require_role
from app.services import dashboard as dashboard_service

router = APIRouter()

@router.get("/api/admin/dashboard")
async def get_dashboard(
    session: AsyncSession = Depends(get_session),
    admin=Depends(require_role("admin")),
):
    return await dashboard_service.get_stats(session)
