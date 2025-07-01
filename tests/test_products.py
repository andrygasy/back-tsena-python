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
async def test_products_crud():
    async with async_session() as session:
        admin = await create_user(session, "admin3@test.com", "pass")
        admin.role = "admin"
        pro = await create_user(session, "pro@test.com", "pass")
        pro.role = "professional"
        await session.commit()
        token_admin = create_access_token({"sub": str(admin.id)})
        token_pro = create_access_token({"sub": str(pro.id)})

    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers_pro = {"Authorization": f"Bearer {token_pro}"}
        headers_admin = {"Authorization": f"Bearer {token_admin}"}

        # unauthorized create
        resp = await ac.post("/api/professional/products", json={"name": "Prod", "price": 10, "stock": 5})
        assert resp.status_code == 401

        # create
        resp = await ac.post(
            "/api/professional/products",
            json={"name": "Prod", "price": 10, "stock": 5},
            headers=headers_pro,
        )
        assert resp.status_code == 201
        prod_id = resp.json()["id"]

        # list public
        resp = await ac.get("/api/products")
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

        # get
        resp = await ac.get(f"/api/products/{prod_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Prod"

        # update
        resp = await ac.put(
            f"/api/professional/products/{prod_id}",
            json={"price": 15},
            headers=headers_pro,
        )
        assert resp.status_code == 200
        assert resp.json()["price"] == 15

        # admin change status
        resp = await ac.put(
            f"/api/admin/products/{prod_id}/status",
            json={"status": "inactive"},
            headers=headers_admin,
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "inactive"

        # delete
        resp = await ac.delete(f"/api/professional/products/{prod_id}", headers=headers_pro)
        assert resp.status_code == 200

        # not found
        resp = await ac.get(f"/api/products/{prod_id}")
        assert resp.status_code == 404
