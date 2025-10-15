# backend/tests/test_payments.py
# Payment processing tests

import pytest
from backend.services.payment import PaymentProcessor


@pytest.fixture
def payment_processor():
    """Create payment processor instance"""
    return PaymentProcessor()


@pytest.mark.asyncio
async def test_payment_processor_initialization(payment_processor):
    """Test payment processor initializes correctly"""
    assert payment_processor is not None
    assert payment_processor.starknet_client is not None


@pytest.mark.asyncio
async def test_get_payment_methods(payment_processor):
    """Test getting payment methods"""
    methods = await payment_processor.get_payment_methods()
    
    assert isinstance(methods, dict)
    assert "methods" in methods
    assert len(methods["methods"]) == 3
    
    # Verify each method has required fields
    for method in methods["methods"]:
        assert "id" in method
        assert "name" in method
        assert "chain" in method
        assert "currency" in method
        assert "fee" in method
        assert "settlement" in method


@pytest.mark.asyncio
async def test_process_starknet_payment(payment_processor):
    """Test Starknet payment processing"""
    tx_hash = await payment_processor.process_starknet_payment(
        from_address="0x123",
        to_address="0x456",
        amount="1.0"
    )
    
    assert isinstance(tx_hash, str)
    assert tx_hash.startswith("0x")
    assert len(tx_hash) > 10


@pytest.mark.asyncio
async def test_process_bitcoin_xverse_payment(payment_processor):
    """Test Bitcoin payment via Xverse"""
    tx_id = await payment_processor.process_bitcoin_payment(
        method="xverse",
        from_address="bc1q123",
        to_address="bc1q456",
        amount=0.001
    )
    
    assert isinstance(tx_id, str)
    assert tx_id.startswith("xverse_")


@pytest.mark.asyncio
async def test_process_bitcoin_vesu_payment(payment_processor):
    """Test Bitcoin payment via Vesu"""
    tx_id = await payment_processor.process_bitcoin_payment(
        method="vesu",
        from_address="bc1q123",
        to_address="bc1q456",
        amount=0.001
    )
    
    assert isinstance(tx_id, str)
    assert tx_id.startswith("vesu_")
