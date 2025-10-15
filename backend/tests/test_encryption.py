# backend/tests/test_encryption.py
# Encryption service tests

import pytest
from backend.services.encryption import EncryptionService


@pytest.fixture
def encryption_service():
    """Create encryption service instance"""
    return EncryptionService()


def test_encryption_service_initialization(encryption_service):
    """Test encryption service initializes correctly"""
    assert encryption_service is not None
    assert encryption_service.cipher is not None


def test_encrypt_decrypt_message(encryption_service):
    """Test message encryption and decryption"""
    original_message = "Hello, this is a secret message!"
    
    # Encrypt
    encrypted = encryption_service.encrypt_message(original_message)
    assert encrypted != original_message
    assert isinstance(encrypted, str)
    
    # Decrypt
    decrypted = encryption_service.decrypt_message(encrypted)
    assert decrypted == original_message


def test_generate_user_key(encryption_service):
    """Test user-specific key generation"""
    user_id = "user123"
    password = "secure_password"
    
    key = encryption_service.generate_user_key(user_id, password)
    
    assert isinstance(key, bytes)
    assert len(key) == 32  # 32 bytes for PBKDF2
    
    # Same inputs should generate same key
    key2 = encryption_service.generate_user_key(user_id, password)
    assert key == key2
    
    # Different inputs should generate different keys
    key3 = encryption_service.generate_user_key("user456", password)
    assert key != key3
