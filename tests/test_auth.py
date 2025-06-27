import asyncio
import pytest
from httpx import AsyncClient

from app.main import app
from app.db.session import engine
from app.models import Base

@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={"email": "user@test.com", "password": "pass"})
        assert response.status_code == 201
        response = await ac.post("/auth/login", json={"email": "user@test.com", "password": "pass"})
        assert response.status_code == 200
        assert "access_token" in response.json()
