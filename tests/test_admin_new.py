import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

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
async def test_admin_hero_slides_and_promotions_and_dashboard():
    async with async_session() as session:
        admin = await create_user(session, "admin@test.com", "pass")
        admin.role = "admin"
        user = await create_user(session, "user@test.com", "pass")
        await session.commit()
        token_admin = create_access_token({"sub": str(admin.id)})
        token_user = create_access_token({"sub": str(user.id)})

    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers_admin = {"Authorization": f"Bearer {token_admin}"}
        headers_user = {"Authorization": f"Bearer {token_user}"}

        # unauthorized hero slide create
        resp = await ac.post("/api/admin/hero-slides", json={"title": "t", "image_url": "i"})
        assert resp.status_code == 401
        resp = await ac.post(
            "/api/admin/hero-slides",
            json={"title": "t", "image_url": "i"},
            headers=headers_user,
        )
        assert resp.status_code == 403

        # create hero slide
        resp = await ac.post(
            "/api/admin/hero-slides",
            json={"title": "Slide", "image_url": "img", "order": 1},
            headers=headers_admin,
        )
        assert resp.status_code == 201
        slide_id = resp.json()["id"]

        # list
        resp = await ac.get("/api/admin/hero-slides", headers=headers_admin)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

        # get
        resp = await ac.get(f"/api/admin/hero-slides/{slide_id}", headers=headers_admin)
        assert resp.status_code == 200
        assert resp.json()["title"] == "Slide"

        # update
        resp = await ac.put(
            f"/api/admin/hero-slides/{slide_id}",
            json={"title": "New"},
            headers=headers_admin,
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "New"

        # delete
        resp = await ac.delete(f"/api/admin/hero-slides/{slide_id}", headers=headers_admin)
        assert resp.status_code == 200
        resp = await ac.get(f"/api/admin/hero-slides/{slide_id}", headers=headers_admin)
        assert resp.status_code == 404

        # promotions
        promo_data = {
            "name": "Promo",
            "discount_type": "percentage",
            "discount_value": 10,
            "start_date": datetime.utcnow().isoformat(),
            "end_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "is_active": True,
        }
        resp = await ac.post("/api/admin/promotions", json=promo_data, headers=headers_admin)
        assert resp.status_code == 201
        promo_id = resp.json()["id"]

        resp = await ac.get("/api/admin/promotions", headers=headers_admin)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

        resp = await ac.get(f"/api/admin/promotions/{promo_id}", headers=headers_admin)
        assert resp.status_code == 200

        resp = await ac.put(
            f"/api/admin/promotions/{promo_id}",
            json={"is_active": False},
            headers=headers_admin,
        )
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False

        resp = await ac.delete(f"/api/admin/promotions/{promo_id}", headers=headers_admin)
        assert resp.status_code == 204

        # dashboard
        resp = await ac.get("/api/admin/dashboard", headers=headers_admin)
        assert resp.status_code == 200
        assert "total_users" in resp.json()

