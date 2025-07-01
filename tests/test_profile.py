import pytest
from httpx import AsyncClient

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
async def test_profile_endpoints():
    async with async_session() as session:
        user = await create_user(session, "profile@test.com", "pass")
        await session.commit()
        token = create_access_token({"sub": str(user.id)})

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # unauthorized access
        resp = await ac.get("/api/profile")
        assert resp.status_code == 401

        headers = {"Authorization": f"Bearer {token}"}
        resp = await ac.get("/api/profile", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["email"] == "profile@test.com"

        resp = await ac.put(
            "/api/profile",
            json={"name": "Tester", "phone": "+33123456789"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Tester"
        assert resp.json()["phone"] == "+33123456789"

        resp = await ac.put(
            "/api/profile",
            json={"phone": "bad-number"},
            headers=headers,
        )
        assert resp.status_code == 422
