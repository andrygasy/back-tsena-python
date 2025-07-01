from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from app.models import User
from app.schemas.profile import UpdateProfile


def get_profile(session: Session, user_id: int) -> User:
    result = session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    return user


def update_profile(
    session: Session, user_id: int, data: UpdateProfile
) -> User:
    result = session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    if data.name is not None:
        user.name = data.name
    if data.phone is not None:
        user.phone = data.phone
    if data.avatar is not None:
        user.avatar = str(data.avatar)

    session.commit()
    session.refresh(user)
    return user
