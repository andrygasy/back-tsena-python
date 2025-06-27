from fastapi import Depends, HTTPException
from app.services.auth import get_current_user


def require_role(role: str):
    async def wrapper(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Accès administrateur requis.")
        return user
    return wrapper
