# backend/tests/test_ai.py
# AI Agent tests

import pytest
from backend.services.ai_agent import AIAgent


@pytest.fixture
def ai_agent():
    """Create AI agent instance"""
    return AIAgent()


@pytest.mark.asyncio
async def test_ai_agent_initialization(ai_agent):
    """Test AI agent initializes correctly"""
    assert ai_agent is not None
    assert ai_agent.vectorstore is not None
    assert ai_agent.qa_chain is not None


@pytest.mark.asyncio
async def test_generate_documentation(ai_agent):
    """Test documentation generation"""
    docs = await ai_agent.generate_documentation(
        game_title="Test RPG",
        description="A test role-playing game"
    )
    
    assert isinstance(docs, dict)
    assert "overview" in docs
    assert "api_reference" in docs
    assert "smart_contracts" in docs
    assert "player_guide" in docs
    assert "setup_guide" in docs
    
    # Verify content
    assert "Test RPG" in docs["overview"]


@pytest.mark.asyncio
async def test_analyze_game(ai_agent):
    """Test game analysis"""
    analysis = await ai_agent.analyze_game_for_publishing("test_game_id")
    
    assert isinstance(analysis, dict)
    assert "status" in analysis
    assert "checks" in analysis
    assert "recommendations" in analysis
    assert "estimated_gas" in analysis


@pytest.mark.asyncio
async def test_optimize_assets(ai_agent):
    """Test asset optimization"""
    optimization = await ai_agent.optimize_assets("test_game_id")
    
    assert isinstance(optimization, dict)
    assert "original_size" in optimization
    assert "optimized_size" in optimization
    assert "reduction" in optimization
    assert "actions" in optimization
