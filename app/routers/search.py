from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas import SearchParams
from app.services import search_service

router = APIRouter()

@router.get("/api/search")
async def search(params: SearchParams = Depends(), session: AsyncSession = Depends(get_session)):
    try:
        return await search_service.search(
            session,
            query=params.q,
            search_type=params.type or "all",
            page=params.page or 1,
            limit=params.limit or 10,
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

