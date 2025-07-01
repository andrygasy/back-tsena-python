import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from uuid import uuid4

from app.main import app
from app.db.session import engine, async_session
from app.models import Base
from app.services.auth import create_user, create_access_token

@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_promotions_errors_and_crud():
    async with async_session() as session:
        admin = await create_user(session, "adminp@test.com", "pass")
        admin.role = "admin"
        user = await create_user(session, "userp@test.com", "pass")
        await session.commit()
        token_admin = create_access_token(str(admin.id))
        token_user = create_access_token(str(user.id))

    async with AsyncClient(app=app, base_url="http://test") as ac:
        valid_data = {
            "name": "Promo",
            "discount_type": "percentage",
            "discount_value": 5,
            "start_date": datetime.utcnow().isoformat(),
            "end_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "is_active": True,
        }

        # unauthorized
        resp = await ac.post("/api/admin/promotions", json=valid_data)
        assert resp.status_code == 401

        # forbidden
        resp = await ac.post(
            "/api/admin/promotions",
            json=valid_data,
            headers={"Authorization": f"Bearer {token_user}"},
        )
        assert resp.status_code == 403

        # invalid dates
        bad = valid_data.copy()
        bad["start_date"], bad["end_date"] = bad["end_date"], bad["start_date"]
        resp = await ac.post(
            "/api/admin/promotions",
            json=bad,
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        assert resp.status_code == 400

        # create
        resp = await ac.post(
            "/api/admin/promotions",
            json=valid_data,
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        assert resp.status_code == 201
        promo_id = resp.json()["id"]

        # not found
        resp = await ac.get(
            f"/api/admin/promotions/{uuid4()}",
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        assert resp.status_code == 404

        # list and detail
        resp = await ac.get("/api/admin/promotions", headers={"Authorization": f"Bearer {token_admin}"})
        assert resp.status_code == 200
        resp = await ac.get(f"/api/admin/promotions/{promo_id}", headers={"Authorization": f"Bearer {token_admin}"})
        assert resp.status_code == 200

        # unauthorized delete
        resp = await ac.delete(f"/api/admin/promotions/{promo_id}")
        assert resp.status_code == 401
