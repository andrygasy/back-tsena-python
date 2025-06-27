from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas import ProfileOut, ProfileUpdate
from app.services import user_service
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/api/profile", response_model=ProfileOut)
async def read_profile(user=Depends(get_current_user)):
    return user

@router.put("/api/profile", response_model=ProfileOut)
async def update_profile(
    data: ProfileUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    updated = await user_service.update_profile(session, user.id, data.name, data.phone, data.avatar)
    return updated
