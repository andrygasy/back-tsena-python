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
async def test_profile_and_admin():
    async with async_session() as session:
        admin = await create_user(session, "admin@test.com", "pass")
        admin.role = "admin"
        user = await create_user(session, "user@test.com", "pass")
        await session.commit()
        token_admin = create_access_token({"sub": str(admin.id)})
        token_user = create_access_token({"sub": str(user.id)})

    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers_admin = {"Authorization": f"Bearer {token_admin}"}
        resp = await ac.get("/api/admin/users", headers=headers_admin)
        assert resp.status_code == 200
        data = resp.json()
        assert "users" in data

        resp = await ac.put(f"/api/admin/users/{user.id}/status", json={"status": "suspended"}, headers=headers_admin)
        assert resp.status_code == 200

        headers_user = {"Authorization": f"Bearer {token_user}"}
        resp = await ac.get("/api/profile", headers=headers_user)
        assert resp.status_code == 200
        resp = await ac.put("/api/profile", json={"name": "Tester"}, headers=headers_user)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Tester"
