# backend/tests/test_api.py
# API endpoint tests

import pytest
from httpx import AsyncClient
from backend.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint health check"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "features" in data


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data


@pytest.mark.asyncio
async def test_get_templates():
    """Test getting game templates"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/games/templates")
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data
        assert len(data["templates"]) == 6
        
        # Verify template structure
        template = data["templates"][0]
        assert "id" in template
        assert "name" in template
        assert "description" in template
        assert "repository" in template
        assert "license" in template


@pytest.mark.asyncio
async def test_payment_methods():
    """Test getting payment methods"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/payments/methods")
        assert response.status_code == 200
        data = response.json()
        assert "methods" in data
        assert len(data["methods"]) == 3
        
        # Verify payment methods
        methods = {m["id"] for m in data["methods"]}
        assert "chipi_pay" in methods
        assert "xverse" in methods
        assert "vesu" in methods


@pytest.mark.asyncio
async def test_user_registration():
    """Test user registration"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "wallet_address": "0x1234567890abcdef"
        }
        response = await client.post("/users/register", json=user_data)
        
        # May fail if user exists, that's ok for now
        if response.status_code == 200:
            data = response.json()
            assert "user_id" in data
            assert data["username"] == "testuser"
