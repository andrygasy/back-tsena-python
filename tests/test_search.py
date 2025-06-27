import pytest
from httpx import AsyncClient

from app.main import app
from app.db.session import engine, async_session
from app.models import Base, Product, Service
from app.services.auth import create_user

@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_search_endpoints(monkeypatch):
    async with async_session() as session:
        user = await create_user(session, "search@test.com", "pass")
        prod = Product(name="Test Phone", price=10, stock=5, user_id=user.id)
        serv = Service(name="Phone Repair", description="Fix phones")
        session.add_all([prod, serv])
        await session.commit()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/search", params={"q": "Phone"})
        assert resp.status_code == 200
        assert resp.json()["pagination"]["total"] >= 2

        resp = await ac.get("/api/search")
        assert resp.status_code == 422

        resp = await ac.get("/api/search", params={"q": "Phone", "type": "products"})
        assert resp.status_code == 200
        assert resp.json()["services"] == []

        resp = await ac.get("/api/search", params={"q": "Phone", "limit": 1, "page": 1})
        assert resp.status_code == 200
        assert resp.json()["pagination"]["limit"] == 1

        async def raise_error(*args, **kwargs):
            raise Exception("boom")

        monkeypatch.setattr("app.services.search_service.search", raise_error)
        resp = await ac.get("/api/search", params={"q": "Phone"})
        assert resp.status_code == 500

