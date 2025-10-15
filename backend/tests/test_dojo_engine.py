# backend/tests/test_dojo_engine.py
# Dojo Engine tests

import pytest
from backend.services.dojo_engine import DojoEngine


@pytest.mark.asyncio
async def test_create_game_world():
    """Test creating a game world"""
    world_address = await DojoEngine.create_game_world("Test Game", "rpg")
    
    assert isinstance(world_address, str)
    assert world_address.startswith("0x")
    assert len(world_address) == 42  # 0x + 40 hex chars


@pytest.mark.asyncio
async def test_deploy_game_contracts():
    """Test deploying game contracts"""
    game_id = "test_game_123"
    world_address = "0x1234567890abcdef"
    
    contracts = await DojoEngine.deploy_game_contracts(game_id, world_address)
    
    assert isinstance(contracts, dict)
    assert "world" in contracts
    assert "game_logic" in contracts
    assert "player_registry" in contracts
    assert "payment_handler" in contracts
    
    # Verify all contract addresses are valid
    for key, address in contracts.items():
        assert address.startswith("0x")


@pytest.mark.asyncio
async def test_get_game_templates():
    """Test getting game templates"""
    templates = await DojoEngine.get_game_templates()
    
    assert isinstance(templates, list)
    assert len(templates) == 6
    
    # Verify template structure
    for template in templates:
        assert "id" in template
        assert "name" in template
        assert "description" in template
        assert "repository" in template
        assert "license" in template
        assert "features" in template
        assert template["license"] == "MIT"
