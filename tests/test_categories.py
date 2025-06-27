import pytest
from httpx import AsyncClient
from uuid import UUID

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
async def test_categories_crud():
    async with async_session() as session:
        admin = await create_user(session, "admin2@test.com", "pass")
        admin.role = "admin"
        user = await create_user(session, "user2@test.com", "pass")
        await session.commit()
        token_admin = create_access_token(str(admin.id))
        token_user = create_access_token(str(user.id))

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # unauthorized
        resp = await ac.post("/api/admin/categories", json={"name": "test"})
        assert resp.status_code == 401

        headers_admin = {"Authorization": f"Bearer {token_admin}"}
        headers_user = {"Authorization": f"Bearer {token_user}"}

        # forbidden for regular user
        resp = await ac.post("/api/admin/categories", json={"name": "test"}, headers=headers_user)
        assert resp.status_code == 403

        # create
        resp = await ac.post("/api/admin/categories", json={"name": "Electronics"}, headers=headers_admin)
        assert resp.status_code == 201
        cat_id = resp.json()["id"]

        # list
        resp = await ac.get("/api/categories")
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

        # get
        resp = await ac.get(f"/api/categories/{cat_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Electronics"

        # update
        resp = await ac.put(f"/api/admin/categories/{cat_id}", json={"description": "Desc"}, headers=headers_admin)
        assert resp.status_code == 200
        assert resp.json()["description"] == "Desc"

        # tree
        resp = await ac.get("/api/categories/tree")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

        # delete
        resp = await ac.delete(f"/api/admin/categories/{cat_id}", headers=headers_admin)
        assert resp.status_code == 200

        # not found
        resp = await ac.get(f"/api/categories/{cat_id}")
        assert resp.status_code == 404
