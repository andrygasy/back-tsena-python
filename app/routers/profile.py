from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas import ProfileOut, UpdateProfile
from app.services import profile as profile_service
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/api/profile", response_model=ProfileOut)
async def read_profile(
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    return await profile_service.get_profile(session, user.id)

@router.put("/api/profile", response_model=ProfileOut)
async def update_profile(
    data: UpdateProfile,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    updated = await profile_service.update_profile(session, user.id, data)
    return updated
