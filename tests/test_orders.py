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
async def test_orders_flow():
    async with async_session() as session:
        admin = await create_user(session, "admin_orders@test.com", "pass")
        admin.role = "admin"
        user = await create_user(session, "buyer@test.com", "pass")
        await session.commit()
        token_admin = create_access_token(str(admin.id))
        token_user = create_access_token(str(user.id))

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # unauthorized create
        resp = await ac.post("/api/orders", json={"items": []})
        assert resp.status_code == 401

        headers_user = {"Authorization": f"Bearer {token_user}"}
        headers_admin = {"Authorization": f"Bearer {token_admin}"}

        # create order
        resp = await ac.post(
            "/api/orders",
            json={"items": [{"product_id": str(UUID(int=1)), "quantity": 2, "price": 5.0}]},
            headers=headers_user,
        )
        assert resp.status_code == 201
        order_id = resp.json()["id"]
        assert resp.json()["total"] == 10.0

        # list user orders
        resp = await ac.get("/api/orders", headers=headers_user)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

        # get order
        resp = await ac.get(f"/api/orders/{order_id}", headers=headers_user)
        assert resp.status_code == 200

        # admin list
        resp = await ac.get("/api/admin/orders", headers=headers_admin)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

        # admin update status
        resp = await ac.put(
            f"/api/admin/orders/{order_id}/status",
            json={"status": "paid"},
            headers=headers_admin,
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "paid"

        # forbidden access to other user's order
        other_headers = {"Authorization": f"Bearer {token_admin}"}
        resp = await ac.get(f"/api/orders/{order_id}", headers=other_headers)
        assert resp.status_code == 403
