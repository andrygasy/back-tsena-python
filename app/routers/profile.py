from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import ProfileOut, UpdateProfile
from app.services import profile as profile_service
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/api/profile", response_model=ProfileOut)
async def read_profile(
    session: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return profile_service.get_profile(session, user.id)

@router.put("/api/profile", response_model=ProfileOut)
async def update_profile(
    data: UpdateProfile,
    session: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    updated = profile_service.update_profile(session, user.id, data)
    return updated
